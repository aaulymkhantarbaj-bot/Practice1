-- functions.sql
CREATE OR REPLACE FUNCTION search_contacts(p_pattern TEXT)
RETURNS TABLE(name TEXT, phone TEXT)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT c.name, c.phone
    FROM contacts AS c
    WHERE c.name ILIKE '%' || p_pattern || '%'
       OR c.phone ILIKE '%' || p_pattern || '%';
END;
$$;