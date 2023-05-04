import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FormField, CustomButton } from '../components';
import { useStateContext } from '../context';
import { ethers } from 'ethers';
import { money } from '../assets';
import { checkIfImage } from '../utils';

const CreateProposal = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  
  // Form field state functions
  const { createProposal } = useStateContext();

  const [form, setForm] = useState({
    name: '',
    title: '',
    description: '',
    target: '',
    deadline: '',
    image: '',
  });

  const handleFormFieldChange = (fieldName, e) => {
    setForm({ ...form, [fieldName]: e.target.value }) // Update every single field
  }

  const handleSubmit = async (e) => {
    e.preventDefault();

    checkIfImage(form.image, async (exists) => {
      if (exists) {
        setIsLoading(true);
        await createProposal({ ...form, target: ethers.utils.parseUnits(form.target, 18)});
        setIsLoading(false);
        navigate('/');
      } else {
        alert('Provide valid image URL')
        setForm({ ...form, image: ''});
      }
    });

    console.log(form);
  }

  return (
    <div className='bg-[#1c1c24] flex justify-center items-center flex-col rounded-[10px] sm:p-10 p-4'>
      {isLoading && 'Loader...'}
      <div className='flex justify-center items-center p-[16px] sm:min-w-[380px] bg-[#3a3a43] rounded-[10px]'>
        <h1 className='font-epilogue font-bold sm:text-[25px] text-[18px] leading-[38px] text-white'>
          Start a Proposal  
        </h1>        
      </div>
      <form onSubmit={handleSubmit} className='w-full mt-[65px] flex flex-col gap-[30px]'>
        <div className='flex flex-wrap gap-[40px]'>
          <FormField 
            labelName="Your Name *"
            placeholder="Liam Arbuckle"
            inputType="text"
            value={form.name}
            handleChange={(e) => handleFormFieldChange('name', e)}
          />
          <FormField 
            labelName="Proposal Title"
            placeholder="What classification are you discussing?"
            inputType="text"
            value={form.title}
            handleChange={(e) => handleFormFieldChange('title', e)}
          />
        </div>
          <FormField 
            labelName="Classification details"
            placeholder="What's your decision for your object and the reasoning behind it?"
            isTextArea
            value={form.description}
            handleChange={(e) => handleFormFieldChange('description', e)}
          />
          <div className='w-full flex justify-start items-center p-4 bg-[#8c6dfd] h-[120px] rounded-[10px]'>
            <img src={money} alt='money' className='w-[40px] h-[40px] object-contain' />
            <h4 className='font-epilogue font-bold text-[25px] text-white ml-[20px]'>You need x votes for the proposal to pass</h4>
          </div>
          <div className="flex flex-wrap gap-[40px]">
            <FormField 
              labelName="Required votes"
              placeholder="10 votes"
              inputType="text"
              value={form.target}
              handleChange={(e) => handleFormFieldChange('target', e)}
            />
            <FormField 
              labelName="End Date"
              placeholder="10th December 1993"
              inputType="date"
              value={form.deadline}
              handleChange={(e) => handleFormFieldChange('deadline', e)}
            />
          </div>
          <FormField 
            labelName="Object Image"
            placeholder="IPFS/opensea link to your object of interest"
            inputType="url"
            value={form.image}
            handleChange={(e) => handleFormFieldChange('image', e)}
          />
          <div className='flex justify-center items-center mt-[40px]'>
            <CustomButton
              btnType='submit'
              title='Submit new proposal'
              styles="bg-[#1dc071]"
            />
          </div>
      </form>
    </div>
  )
}

export default CreateProposal;