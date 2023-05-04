import React from 'react';
import { useNavigate } from 'react-router-dom';
import FundCard from './FundCard';
import { loader } from '../assets';

const DisplayProposals = ({ title, isLoading, proposals }) => {
  const navigate = useNavigate();

  const handleNavigate = (proposal) => {
    navigate(`/proposal-details/${proposal.title}`, { state: proposal })
  }
  
  return (
    <div>
      <h1 className="font-epilogue font-semibold text-[18px] text-white text-left">{title} ({proposals.length})</h1>

      <div className="flex flex-wrap mt-[20px] gap-[26px]">
        {isLoading && (
          <img src={loader} alt="loader" className="w-[100px] h-[100px] object-contain" />
        )}

        {!isLoading && proposals.length === 0 && (
          <p className="font-epilogue font-semibold text-[14px] leading-[30px] text-[#818183]">
            You have not created any proposals yet
          </p>
        )}

        {!isLoading && proposals.length > 0 && proposals.map((proposal) => <FundCard 
          key={proposal.id}
          {...proposal}
          handleClick={() => handleNavigate(proposal)}
        />)}
      </div>
    </div>
  )
}

export default DisplayProposals;