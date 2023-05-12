import { useEffect, useState } from "react";
import { supabase } from '../../api/supabaseClient';
import Auth from '../components/Auth/Auth';
import Play from './play';
import Account from '../components/Auth/Account';

function Authenticate() {
    const [session, setSession] = useState(null);
    useEffect(() => {
        setSession(supabase.auth.session());
        supabase.auth.onAuthStateChange((_event, session) => {
            setSession(session);
        })
    }, []);

    return (
        <div className="container mx-auto">
            {!session ? <Auth /> : <Account key={session.user.id} session={session} />}
            <Play />
        </div>
    );
}

export default Authenticate;