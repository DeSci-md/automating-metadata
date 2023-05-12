import {
  ConnectWallet,
  useAddress,
  useContract,
  useMetamask,
} from "@thirdweb-dev/react";
import React, { useEffect, useState } from "react";
import CurrentGear from "../components/Ansible/CurrentGear";
import LoadingSection from "../components/Ansible/LoadingSection";
import OwnedGear from "../components/Ansible/OwnedGear";
import Rewards from "../components/Ansible/Rewards";
import Shop from "../components/Ansible/Shop";
import {
  CHARACTER_EDITION_ADDRESS,
  GOLD_GEMS_ADDRESS,
  MINING_CONTRACT_ADDRESS,
  PICKAXE_EDITION_ADDRESS,
} from "../lib/contractAddresses";
import styles from "../styles/Home.module.css";

import Dao from "../components/dao";
import Auth from "../components/Auth/Auth";
import { supabase } from "../../api/supabaseClient";
import PlanetBreadboard from '../components/Controller/Planet';

export default function Play() {
  const address = useAddress();

  const { contract: miningContract } = useContract(MINING_CONTRACT_ADDRESS);
  const { contract: characterContract } = useContract(
    CHARACTER_EDITION_ADDRESS,
    "edition-drop"
  );
  const { contract: pickaxeContract } = useContract(
    PICKAXE_EDITION_ADDRESS,
    "edition-drop"
  );
  const { contract: tokenContract } = useContract(GOLD_GEMS_ADDRESS, "token");

  if (!address) {
    return (
      <div className={styles.container}>
        <ConnectWallet colorMode="dark" />
      </div>
    );
  }
  

  /* Supabase authentication components
  const [session, setSession] = useState(null);
  useEffect(() => {
    setSession(supabase.auth.session())
    supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })
  }, [])*/

  return (
    <div className={styles.container}>
        {/*<Auth /> */}
        <Dao />
        <PlanetBreadboard />
        {miningContract &&
        characterContract &&
        tokenContract &&
        pickaxeContract ? (
          <div className={styles.mainSection}>
            <CurrentGear
              miningContract={miningContract}
              characterContract={characterContract}
              pickaxeContract={pickaxeContract}
            />
            <Rewards
              miningContract={miningContract}
              tokenContract={tokenContract}
            />
          </div>
        ) : (
          <LoadingSection />
        )}

        <hr className={`${styles.divider} ${styles.bigSpacerTop}`} />

        {pickaxeContract && miningContract ? (
          <>
            <h2 className={`${styles.noGapTop} ${styles.noGapBottom}`}>
              Your Owned Pickaxes
            </h2>
            <div
              style={{
                width: "100%",
                minHeight: "10rem",
                display: "flex",
                flexDirection: "row",
                justifyContent: "center",
                alignItems: "center",
                marginTop: 8,
              }}
            >
              <OwnedGear
                pickaxeContract={pickaxeContract}
                miningContract={miningContract}
              />
            </div>
          </>
        ) : (
          <LoadingSection />
        )}

        <hr className={`${styles.divider} ${styles.bigSpacerTop}`} />

        {pickaxeContract && tokenContract ? (
          <>
            <h2 className={`${styles.noGapTop} ${styles.noGapBottom}`}>Shop</h2>
            <div
              style={{
                width: "100%",
                minHeight: "10rem",
                display: "flex",
                flexDirection: "row",
                justifyContent: "center",
                alignItems: "center",
                marginTop: 8,
              }}
            >
              <Shop pickaxeContract={pickaxeContract} />
            </div>
            
          </>
        ) : (
          <LoadingSection />
        )}
      </div>
    /*<div className="container mx-auto">
       {!session ? <Auth /> : <Account key={session.user.id} session={session} />} 
      Maybe move everything below into a new component, and then set that component in the place of <Account key.... />
      */
  );
}
