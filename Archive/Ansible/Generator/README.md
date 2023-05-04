# sytizen-unity
[![.github/workflows/moralis.yml](https://github.com/Signal-K/sytizen/actions/workflows/moralis.yml/badge.svg?branch=ansible)](https://github.com/Signal-K/sytizen/actions/workflows/moralis.yml)
[![Node.js CI](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml/badge.svg)](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml)
[![Node.js CI](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml/badge.svg?branch=wb3-7--interacting-with-anomalies-from-smart)](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml)
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/signal-k/sytizen/HEAD)
[![](https://github.com/Signal-K/sytizen/actions/workflows/node.js.yml/badge.svg?branch=wb3-7--interacting-with-anomalies-from-smart)](https://deepnote.com/workspace/star-sailors-49d2efda-376f-4329-9618-7f871ba16007/project/Supabase-Talk-ab6b31e5-13c3-4949-af38-1197d00bd4d1/notebook/Flask%20API-cb9219547b9e4e228b15cbf8a1aa9cf4#99de0381ef0d40ffaee2354354861bae)
[![](https://badges.thirdweb.com/contract?address=0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004&theme=light&chainId=5)](https://thirdweb.com/goerli/0xCcaA1ABA77Bae6296D386C2F130c46FEc3E5A004?utm_source=contract_badge)

# Signal-K/Sytizen Repo
## Related repositories
* [Signal-K/polygon](https://github.com/Signal-K/polygon/issues/26) ↝ Contract interactions
* [Signal-K/client](https://github.com/Signal-K/client) ↝ Frontend for interactions with our contracts

## Documentation
All documentation is visible on [Notion](https://www.notion.so/skinetics/Sample-Planets-Contract-4c3bdcbca4b9450382f9cc4e72e081f7)

# Citizen Science Classifications
## Process
* User mints an anomaly that has appeared in their UI (for now, the webapp, later it will be the game as well)
* API searches for a token that has already been lazy minted with the TIC id of the anomaly (or the identifier of the candidate)
  * If there is a token id that has the TIC Id, then claim a copy of that to the `msg.sender` (player’s address) so they can manipulate it in-game
  * If the TIC ID has never been minted before, lazy mint a new one with parameters fetched from the data source and send it to `msg.sender`
  * Return the IPFS metadata
* Add some buttons that allow manipulations for the NFT (e.g. viewing (reading) metadata (e.g. image/video files, graphs).
  * Graphs should be generated in a Jupyter notebook and returned in the Next app.
* User creates post (proposal [Proposal Board → Migration from Vite](https://www.notion.so/Proposal-Board-Migration-from-Vite-2e3ef95e384d4ac1875e0dbbe9a59337)) with the NFT ID for their anomaly and some extra metadata for their discoveries and proposal, and then users can vote