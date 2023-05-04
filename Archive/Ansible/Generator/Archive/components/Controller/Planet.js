import { supabase } from "../../pages/supabaseClient";
import { ConnectWallet, ThirdwebNftMedia, useContract, useNFTs, useOwnedNFTs, useAddress, Web3Button } from "@thirdweb-dev/react";

import { Container } from "semantic-ui-react";

const PlanetBreadboard = () => { //  { session } 
    // Eth/contract hooks ====>
    const { contract } = useContract("0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9"); // Add contract of collection as hook
    const contractAddressKey = "0xed6e837Fda815FBf78E8E7266482c5Be80bC4bF9";
    const address = useAddress(); // get the address of connected user
    const { data: nfts } = useOwnedNFTs(contract, address); // Array of nfts

    return (
        <Container>
            <ConnectWallet />
            <hr />
            <Web3Button
                contractAddress={contractAddressKey}
                action={(contract) => contract.call("claim", address, 0, 1)}
            >
                Claim a planet
            </Web3Button>
            {nfts?.map((nft) => (<div>
                <ThirdwebNftMedia
                    key={nft.metadata.id.toString()}
                    metadata={nft.metadata}
                />
                <h2>{nft.metadata.name}</h2>
            </div>))}
        </Container>
    );
}

export default PlanetBreadboard;