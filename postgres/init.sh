#!/bin/bash
set -e
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE TABLE IF NOT EXISTS audit_transactions (
        id SERIAL PRIMARY KEY,
        sender_account VARCHAR(34) NOT NULL,
        recipient_account VARCHAR(34) NOT NULL,
        amount NUMERIC(12, 2) NOT NULL,
        currency VARCHAR(3) DEFAULT 'XOF',
        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
    );
    INSERT INTO audit_transactions (sender_account, recipient_account, amount) VALUES
    ('CI0340100112345678901234', 'BJ0610100198765432109876', 150000.00),
    ('BJ0610100198765432109876', 'SN0120100155555555555555', 45000.00);
    CREATE USER agent_readonly WITH PASSWORD '$AGENT_READONLY_PASSWORD';
    GRANT CONNECT ON DATABASE $POSTGRES_DB TO agent_readonly;
    GRANT USAGE ON SCHEMA public TO agent_readonly;
    GRANT SELECT ON audit_transactions TO agent_readonly;
EOSQL
