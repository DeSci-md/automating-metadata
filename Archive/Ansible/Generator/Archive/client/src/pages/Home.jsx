import React, { useState, useEffect } from 'react';
import { useStateContext } from '../context';
import { DisplayProposals } from '../components';

const Home = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [proposals, setProposals] = useState([]);

  const { address, contract, getProposals }  = useStateContext();
  const fetchProposals = async () => { // This is to allow us to call this g.request in the useEffect (as the request is async in /context)
    setIsLoading(true);
    const data = await getProposals();
    setProposals(data);
    setIsLoading(false);
  }

  useEffect(() => {
    if (contract) fetchProposals();
  }, [address, contract]); // Re-called when these change

  return (
    <DisplayProposals // Component that selects different proposals based on props passed here
      title="All Proposals"
      isLoading={isLoading}
      proposals={proposals}
    />
  )
}

export default Home;