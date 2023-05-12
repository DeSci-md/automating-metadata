import { useAddress, ConnectWallet, Web3Button, useContract, useNFTBalance } from '@thirdweb-dev/react';
import { useState, useEffect, useMemo } from 'react';
import styles from '../styles/Dao.module.css';
import { AddressZero } from "@ethersproject/constants";
//import CreateProposal from '../components/Meta/CreateProposal';

const Dao = () => {
    const address = useAddress();
    console.log("🤝 User address: ", address);

    if (!address) {
        return (
            <div className={styles.landing}>
                <h1>Welcome to Star Sailors DAO</h1>
                <div className={styles.btnhero}>
                    <ConnectWallet />
                </div>
            </div>
        );
    }

    const editionDropAddress = '0x93FC4ba29c41c059fB9f4727F3903df776771Af8';
    const tokenAddress = "0x6e4A2c27a080ae51C825e7b08D753D8851F9a455";
    const { contract: editionDrop } = useContract(editionDropAddress, "edition-drop");
    const { contract: token } = useContract(tokenAddress, 'token');
    const { contract : vote } = useContract("0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9", 'vote');
    const { data: nftBalance } = useNFTBalance(editionDrop, address, "0"); // Hook to check if authenticated user has membership nft
    
    const hasClaimedNFT = useMemo(() => {
        return nftBalance && nftBalance.gt(0);
    }, [nftBalance]);
    
    const [memberTokenAmounts, setMemberTokenAmounts] = useState([]);
    const [memberAddresses, setMemberAddresses] = useState([]);
    const shortenAddress = (str) => {
        return str.substring(0, 6) + '...' + str.substring(str.length - 4);
    };

    const [proposals, setProposals] = useState([]);
    const [isVoting, setIsVoting] = useState(false);
    const [hasVoted, setHasVoted] = useState(false);

    useEffect(() => {
        if (!hasClaimedNFT) {
            return;
        }

        const getAllProposals = async () => {
            try {
                const proposals = await vote.getAll();
                setProposals(proposals);
                console.log("🌈 Proposals: ", proposals);
            } catch (error) {
                console.log("Failed to get proposals. ", error);
            }
        };
        getAllProposals();
    }, [hasClaimedNFT, vote]);

    useEffect(() => { // Check if user has already voted
        if (!hasClaimedNFT) {
            return;
        }

        if (!proposals.length) {
            return;
        }

        const checkIfUserHasVoted = async () => {
            try {
                const hasVoted = await vote.hasVoted(proposals[0].proposalId, address);
                setHasVoted(hasVoted);
                if (hasVoted) {
                    console.log("User has already voted");
                } else {
                    console.log("User has not voted yet");
                }
            } catch (error) {
                console.error("Failed to check if wallet has voted. ", error);
            }
        };
        checkIfUserHasVoted();
    }, [hasClaimedNFT, proposals, address, vote]);

    useEffect(() => { // get nft holdings of each user for token id 0
        if (!hasClaimedNFT) {
            return;
        }

        const getAllAddresses = async () => {
            try {
                const memberAddresses = await editionDrop?.history.getAllClaimerAddresses(0,);
                setMemberAddresses(memberAddresses);
                console.log('🦔 Member address: ', memberAddresses);
            } catch (error) {
                console.error('failed to get member list -> ', error);
            }
        };
        getAllAddresses();
    }, [hasClaimedNFT, editionDrop?.history]);

    useEffect(() => { // Get token holdings of each user
        if (!hasClaimedNFT) {
            return;
        }

        const getAllBalances = async () => {
            try {
                const amounts = await token?.history.getAllHolderBalances();
                setMemberTokenAmounts(amounts);
                console.log('🔐 Amounts: ', amounts);
            } catch (error) {
                console.error('Failed to get member balances ', error);
            }
        };
        getAllBalances();
    }, [hasClaimedNFT, token?.history]);

    const memberList = useMemo(() => {
        return memberAddresses.map((address) => {
            const member = memberTokenAmounts?.find(({ holder }) => holder === address);

            return {
                address,
                tokenAmount: member?.balance.displayValue || '0',
            };
        });
    }, [memberAddresses, memberTokenAmounts]);

    if (hasClaimedNFT) {
        return (
          <div className="member-page">
            <h1>🍪DAO Member Page</h1>
            <p>Congratulations on being a member</p>
            <div>
              <div>
                <h2>Member List</h2>
                <table className="card">
                  <thead>
                    <tr>
                      <th>Address</th>
                      <th>Token Amount</th>
                    </tr>
                  </thead>
                  <tbody>
                    {memberList.map((member) => {
                      return (
                        <tr key={member.address}>
                          <td>{shortenAddress(member.address)}</td>
                          <td>{member.tokenAmount}</td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
              <div>
                <h2>Active Proposals</h2>
                <form
                  onSubmit={async (e) => {
                    e.preventDefault();
                    e.stopPropagation();
    
                    //before we do async things, we want to disable the button to prevent double clicks
                    setIsVoting(true);
    
                    // lets get the votes from the form for the values
                    const votes = proposals.map((proposal) => {
                      const voteResult = {
                        proposalId: proposal.proposalId,
                        //abstain by default
                        vote: 2,
                      };
                      proposal.votes.forEach((vote) => {
                        const elem = document.getElementById(
                          proposal.proposalId + '-' + vote.type,
                        );
    
                        if (elem.checked) {
                          voteResult.vote = vote.type;
                          return;
                        }
                      });
                      return voteResult;
                    });
    
                    // first we need to make sure the user delegates their token to vote
                    try {
                      //we'll check if the wallet still needs to delegate their tokens before they can vote
                      const delegation = await token.getDelegationOf(address);
                      // if the delegation is the 0x0 address that means they have not delegated their governance tokens yet
                      if (delegation === AddressZero) {
                        //if they haven't delegated their tokens yet, we'll have them delegate them before voting
                        await token.delegateTo(address);
                      }
                      // then we need to vote on the proposals
                      try {
                        await Promise.all(
                          votes.map(async ({ proposalId, vote: _vote }) => {
                            // before voting we first need to check whether the proposal is open for voting
                            // we first need to get the latest state of the proposal
                            const proposal = await vote.get(proposalId);
                            // then we check if the proposal is open for voting (state === 1 means it is open)
                            if (proposal.state === 1) {
                              // if it is open for voting, we'll vote on it
                              return vote.vote(proposalId, _vote);
                            }
                            // if the proposal is not open for voting we just return nothing, letting us continue
                            return;
                          }),
                        );
                        try {
                          // if any of the propsals are ready to be executed we'll need to execute them
                          // a proposal is ready to be executed if it is in state 4
                          await Promise.all(
                            votes.map(async ({ proposalId }) => {
                              // we'll first get the latest state of the proposal again, since we may have just voted before
                              const proposal = await vote.get(proposalId);
    
                              //if the state is in state 4 (meaning that it is ready to be executed), we'll execute the proposal
                              if (proposal.state === 4) {
                                return vote.execute(proposalId);
                              }
                            }),
                          );
                          // if we get here that means we successfully voted, so let's set the "hasVoted" state to true
                          setHasVoted(true);
                          // and log out a success message
                          console.log('successfully voted');
                        } catch (err) {
                          console.error('failed to execute votes', err);
                        }
                      } catch (err) {
                        console.error('failed to vote', err);
                      }
                    } catch (err) {
                      console.error('failed to delegate tokens');
                    } finally {
                      // in *either* case we need to set the isVoting state to false to enable the button again
                      setIsVoting(false);
                    }
                  }}
                >
                  {proposals.map((proposal) => (
                    <div key={proposal.proposalId} className="card">
                      <h5>{proposal.description}</h5>
                      <div>
                        {proposal.votes.map(({ type, label }) => (
                          <div key={type}>
                            <input
                              type="radio"
                              id={proposal.proposalId + '-' + type}
                              name={proposal.proposalId}
                              value={type}
                              //default the "abstain" vote to checked
                              defaultChecked={type === 2}
                            />
                            <label htmlFor={proposal.proposalId + '-' + type}>
                              {label}
                            </label>
                          </div>
                        ))}
                      </div>
                    </div>
                  ))}
                  <button disabled={isVoting || hasVoted} type="submit">
                    {isVoting
                      ? 'Voting...'
                      : hasVoted
                      ? 'You Already Voted'
                      : 'Submit Votes'}
                  </button>
                  {!hasVoted && (
                    <small>
                      This will trigger multiple transactions that you will need to
                      sign.
                    </small>
                  )}
                </form>
                <img src='/Sytizen-Tests/p1.png' height="64" width="64"/> {/* If you vote, you then get an nft, which allows you to stake. Maybe a button that executes two functions? NFT gate a page, claim that nft by classifying, then allow staking on that planet. Create a new nft id, attach that to the player table, and pass it into Flask. */}
                {/*<CreateProposal />*/}
              </div>
            </div>
          </div>
        );
      }

    return (
        <div className={styles.landing}>
            <h1>👀 Mint your DAO membership</h1>
            <div className={styles.btnhero}>
                <Web3Button
                    contractAddress={editionDropAddress}
                    action={contract => {
                        contract.erc1155.claim(0, 1)
                    }}
                    onSuccess={() => {
                        console.log(`🌊 Successfully Minted! Check it out on OpenSea: https://testnets.opensea.io/assets/${editionDrop.getAddress()}/0`);
                    }}
                    onError={error => {
                        console.error("Failed to mint NFT, ", error);
                    }}
                >
                    Mint your membership NFT (FREE)
                </Web3Button>
            </div>
        </div>
    );
}

export default Dao;