-- Insert initial administrator user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES ('36c9050e-ddd3-4c3b-9731-9f487208bbc1', 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$10tnFeq.ZF1DtMCj8ofW0..Cg3jkaVMaSwG4r6F4/L0zeXkKtD9wC', TRUE);

-- Insert initial amenities
INSERT INTO amenities (id, name) VALUES
  ('4344c715-63c2-4d82-aad0-bf1423559be1', 'WiFi'),
  ('c9381f19-2a74-40f7-814c-83e15f9dd47e', 'Swimming Pool'),
  ('7f8b606b-48ae-4023-af05-1fcba6932e2f', 'Air Conditioning');
