import sdk from "./1-initialize-sdk.mjs";

(async () => {
    try {
        const vote = await sdk.getContract("0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9", 'vote');
        const token = await sdk.getContract("0x6e4A2c27a080ae51C825e7b08D753D8851F9a455", 'token');
        await token.roles.grant("minter", vote.getAddress()); // Treasury has power to mint additional tokens if needed
        console.log(
            "Successfully gave vote contract permissions to act on token contract"
        );
    } catch (error) {
        console.error(
            "failed to grant vote contract permissions on token contract",
            error
        );
        process.exit(1);
    }

    try {
        const vote = await sdk.getContract("0x267239EA5C955D2681652a2B9c6AAbD6f8207Cc9", "vote");
        const token = await sdk.getContract("0x6e4A2c27a080ae51C825e7b08D753D8851F9a455", 'token');
        const ownedTokenBalance = await token.balanceOf(process.env.WALLET_ADDRESS);
        const ownedAmount = ownedTokenBalance.displayValue;
        const percent90 = Number(ownedAmount) / 100 * 90;

        await token.transfer(
            vote.getAddress(),
            percent90
        );
        console.log("✅ Successfully transferred " + percent90 + " tokens to vote contract");
    } catch (err) {
        console.error("failed to transfer tokens to vote contract", err);
    }
})();

/* Output: 
👋 -> SDK Initialised by address:  0x15A4C3b42f3386Cd1A642908525469684Cac7C6d
Successfully gave vote contract permissions to act on token contract
✅ Successfully transferred 1800000 tokens to vote contract
*/