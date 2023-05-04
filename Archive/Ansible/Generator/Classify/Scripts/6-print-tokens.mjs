import sdk from "./1-initialize-sdk.mjs";

(async () => {
    try {
        const token = await sdk.getContract("0x6e4A2c27a080ae51C825e7b08D753D8851F9a455", 'token');
        const amount = 1_000_000;
        await token.mint(amount);
        const totalSupply = await token.totalSupply();
        console.log("✅ There now are ", totalSupply.displayValue, " $SAILORS in circulation");
    } catch (error) {
        console.error("Failed to print tokens, ", error);
    }
})();