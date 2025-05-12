-- Add is_seller column if it doesn't exist
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns 
                  WHERE table_name = 'users' AND column_name = 'is_seller') THEN
        ALTER TABLE users ADD COLUMN is_seller BOOLEAN NOT NULL DEFAULT false;
    END IF;
END $$;

-- Drop role column if it exists
DO $$ 
BEGIN 
    IF EXISTS (SELECT 1 FROM information_schema.columns 
              WHERE table_name = 'users' AND column_name = 'role') THEN
        ALTER TABLE users DROP COLUMN role;
    END IF;
END $$;

-- Make username unique if it's not already
DO $$ 
BEGIN 
    IF NOT EXISTS (SELECT 1 FROM information_schema.table_constraints 
                  WHERE table_name = 'users' AND constraint_name = 'users_username_key') THEN
        ALTER TABLE users ADD CONSTRAINT users_username_key UNIQUE (username);
    END IF;
END $$; 