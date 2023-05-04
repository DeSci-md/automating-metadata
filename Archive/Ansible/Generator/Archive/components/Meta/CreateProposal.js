import { useState, useEffect } from "react";
import { supabase } from "../../pages/supabaseClient";

import { ThirdwebSDK } from "@thirdweb-dev/sdk";

const sdk = new ThirdwebSDK("mumbai");
const contract = await sdk.getContract("0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9", "vote");
const executions = [
    {
        // The contract you want to make a call to
        toAddress: "0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9",
        // The amount of the native currency to send in this transaction
        nativeTokenValue: 0,
        // Transaction data that will be executed when the proposal is executed
        // This is an example transfer transaction with a token contract (which you would need to setup in code)
        transactionData: tokenContract.encoder.encode("transfer", [
            fromAddress,
            amount,
        ]),
    },
];

const proposal = await contract.propose(description, executions);

const CreateProposal = () => {
    const [description, setDescription] = useState(""); // The vote content
    const sendDescription = () => {
        console.log(description);
    } // For now, just link user to this page: https://thirdweb.com/mumbai/0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9/proposals (to create a proposal). Could send it to Supabase and execute it from there?

    return (
        <div aria-live='polite' className="container mx-auto">
            <h1>Create a proposal for the DAO</h1>
            <form onSubmit={sendDescription} className='form-widgets'>
                <div class='container mx-auto w-102 py-4'>
                    <input type='text'
                        name='text'
                        id='username'
                        class="mt-1 px-3 py-2 bg-white border shadow-sm border-slate-300 placeholder-slate-400 focus:outline-none focus:border-sky-500 focus:ring-sky-500 block w-full rounded-md sm:text-sm focus:ring-1"
                        placeholder="What are you wanting to put to a vote?"
                        value={description || ''}
                        onChange={(e) => setDescription(e.target.value)}
                    />
                </div>
                <div classname='text-center'>
                    <button class='w-44 h-11 rounded-full text-gray-50 bg-indigo-600 hover:bg-indigo-700'>
                        Create vote
                    </button>
                </div>
            </form>
        </div>
    )
}

export default CreateProposal;