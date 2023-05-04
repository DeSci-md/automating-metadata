/* This will reference the current user profile structure in gizmotronn/comments & signal-k/client (off-chain), but will be updated to add on-chain user data down the line */
CREATE TABLE public.playerList ( /* Will reference/duplicate what is on Supabase, and this migration will then be added to Flask */
    id integer NOT NULL,
    username text NOT NULL,
    /*updated_at timestampz NOT NULL,*/
    full_name text NOT NULL,
    avatar_url text NOT NULL, /* URI on supabase storage */
    website text NOT NULL,
    address text NOT NULL,
    PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
);

INSERT INTO playerList(id, username, full_name, avatar_url, website, address) /* This will be duplicated in Flask -> initially adding the user address to an existing record */
VALUES
    (1, 'liam', 'liam arbuckle', '', '', '') /* Example data -> no point adding real data as it will just be overwritten by interacting with the API anyway */