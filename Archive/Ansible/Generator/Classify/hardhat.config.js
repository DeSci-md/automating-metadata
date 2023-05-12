/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: '0.8.11',
    defaultNetwork: 'goerli',
    networks: {
      hardhat: {},
      goerli: {
        url: "https://rpc.ankr.com/eth_goerli",
        accounts: [`0x${process.env.walletPrivateKey}`]
      },
    },
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
};
