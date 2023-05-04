import React, { useState, useEffect } from 'react';
import { useLocation } from 'react-router-dom';
import { ethers } from 'ethers';
import { useStateContext } from '../context';
import { CustomButton, CountBox } from '../components';
import { calculateBarPercentage, daysLeft } from '../utils';
import { thirdweb } from '../assets';

const ProposalDetails = () => {
  const { state } = useLocation();
  const { vote, getVotes, contract, address } = useStateContext();
  console.log(state);

  const [isLoading, setIsLoading] = useState(false);
  const [amount, setAmount] = useState('');
  const [voters, setVoters] = useState([]); // Array of voters on a specific proposal
  const remainingDays = daysLeft(state.deadline);

  const fetchVoters = async () => {
    const data = await getVotes(state.pId);
    setVoters(data);
  }

  useEffect(() => {
    if(contract) fetchVoters();
  }, [contract, address]);

  const handleVote = async () => {
    setIsLoading(true);

    await vote(state.pId, amount); 

    navigate('/')
    setIsLoading(false);
  }

  return (
    <div>
      {isLoading && 'Loading...'}
      <div className='w-full flex md:flex-row flex-col mt-10 gap-[30px]'>
        <div className='flex-1 flex-col'>
          <img src={state.image} alt='campaign' className='w-full h-[410px] object-cover rounded-xl' />
          <div className='relative w-full h-[5px] bg-[#3a3a43] mt-2'>
            <div className='absolute h-full bg-[#41cd8d]' style={{ width: `${calculateBarPercentage(state.target, state.amountCollected)}%`, maxWidth: '100%' }}>
            </div>
          </div>
        </div>
        <div className='flex md:w-[150px] w-full flex-wrap justify-between gap-[30px]'>
          <CountBox title='Days Left' value={remainingDays} />
          <CountBox title={`Raised of ${state.target}`} value={state.amountCollected} />
          <CountBox title='Voters' value={voters.length} />
        </div>
      </div>
      <div className='mt-[60px] flex lg:flex-row flex-col gap-5'>
        <div className='flex-[2] flex flex-col gap-[40px]'>
          <div>
            <h4 className='font-epilogue font-semibold text-[18px] text-white uppercase'>CREATOR:</h4>
            <div className='mt-[20px] flex flex-row items-center flex-wrap gap-[14px]'>
              <div className='w-[52px] h-[52px] flex items-center justify-center rounded-full bg-[#2c2f32] cursor-pointer'>
                <img src={thirdweb} alt='user profilepic' className='w-[60%] h-[60%] object-contain' />
              </div>
              <div>
                <h4 className='font-epilogue font-semibold text-[14px] text-white break-all'>{state.owner}</h4>
                <p className='mt-[4px] font-epilogue font-normal text-[12px] text-[#808191]'>10 Proposals</p>
              </div>
            </div>
          </div>
          <div>
            <h4 className='font-epilogue font-semibold text-[18px] text-white uppercase'>STORY:</h4>
            <div className='mt-[20px]'>
              <p className='font-epilogue font-normal text-[16px] text-[#808191] leading-[26px] text-justify'>{state.description}</p>
            </div>
          </div>
          <div>
            <h4 className='font-epilogue font-semibold text-[18px] text-white uppercase'>VOTERS:</h4>
            <div className='mt-[20px] flex flex-col gap-4'>
              {voters.length > 0 ? voters.map((item, index) => {
                <div>
                  VOTER
                </div>
              }) : (
                <p className='font-epilogue font-normal text-[16px] text-[#808191] leading-[26px] text-justify'>Nobody has voted on this proposal yet</p>
              )}
            </div>
          </div>
        </div>
        <div className='flex-1'>
          <h4 className='font-epilogue font-semibold text-[18px] text-white uppercase'>Votes</h4>
          <div className='my-[20px] flex flex-col p-4 bg-[#1c1c24] rounded-[10px]'>
            <p className='font-epilogue font-medium text-[20px] leading-[30px] text-center text-[#808191]'>Vote for this proposal</p>
            <div className='mt-[30px]'>
              <input 
                type="number"
                placeholder="ETH 0.1"
                step="0.01"
                className="w-full py-[10px] sm:px-[20px] px-[15px] outline-none border-[1px] border-[#3a3a43] bg-transparent font-epilogue text-white text-[18px] leading-[30px] placeholder:text-[#4b5264] rounded-[10px]"
                value={amount}
                onChange={(e) => setAmount(e.target.value)}
              />
              <div className='my-[20px] p-4 bg-[#13131a] rounded-[10px]'>
                <h4 className='font-epilogue font-semibold text-[14px] leading-[22px] text-white'>Vote for this proposal with NO comments or adjustments</h4>
              </div>
              <CustomButton
                btnType='button'
                title='Vote for proposal'
                styles='w-full bg-[#8c6dfd]'
                handleClick={handleVote}
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default ProposalDetails;