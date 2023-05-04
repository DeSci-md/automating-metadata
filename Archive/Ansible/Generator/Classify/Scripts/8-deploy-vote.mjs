import sdk from './1-initialize-sdk.mjs';

(async () => {
    try {
        const voteContractAddress = await sdk.deployer.deployVote({
            name: "Star Sailors DAO",
            voting_token_address: "0x6e4A2c27a080ae51C825e7b08D753D8851F9a455",
            voting_delay_in_blocks: 0,
            voting_period_in_blocks: 6570,
            voting_quorum_fraction: 0,
            proposal_token_threshold: 0,
        });

        console.log("✅ Successfully deployed vote contract, address: ", voteContractAddress,);
    } catch (err) {
        console.error("Failed to deploy vote contract, ", err);
    }
})();

/* Output:
👋 -> SDK Initialised by address:  0x15A4C3b42f3386Cd1A642908525469684Cac7C6d
✅ Successfully deployed vote contract, address:  0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9
*/