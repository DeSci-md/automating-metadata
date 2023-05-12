import sdk from "./1-initialize-sdk.mjs";
import { readFileSync } from 'fs';

(async () => {
    try { // Update `editionDrop` variable with address received when running `2-deploy-drop.mjs`
        const editionDrop = await sdk.getContract("0x93FC4ba29c41c059fB9f4727F3903df776771Af8", 'edition-drop');
        await editionDrop.createBatch([
            {
                name: "Spiritful Photoreceptor Patch",
                description: 'This NFT gives you access to our community DAO, AND a special eyepatch',
                image: readFileSync("assets/ContributorCard.png"),
            },
        ]);
        console.log("✅ Successfully created a new NFT in the drop!");
    } catch (error) {
        console.error("failed to create the new NFT", error);
    }
})();