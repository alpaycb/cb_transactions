CREATE SCOPE `bankAccounts`.`clientScope`; 
CREATE COLLECTION `bankAccounts`.`clientScope`.`accountingInfo`;
 
INSERT INTO `bankAccounts`.`clientScope`.`accountingInfo` (KEY, VALUE) 
VALUES 
("account_001", {"accountName": "Hans Müller", "accountNumber": "123456789", "accountType": "savings", "balance": 1000.00}), 
("account_002", {"accountName": "Thomas Mann", "accountNumber": "987654321", "accountType": "checking", "balance": 2500.00}), 
("account_003", {"accountName": "Felix Muster", "accountNumber": "112233445", "accountType": "savings", "balance": 1500.00}), 
("account_004", {"accountName": "Andreas Kaufmann", "accountNumber": "556677889", "accountType": "checking", "balance": 3000.00}), 
("account_005", {"accountName": "Edith Piaff", "accountNumber": "998877665", "accountType": "savings", "balance": 500.00}), 
("account_006", {"accountName": "Thomas Edison", "accountNumber": "443322110", "accountType": "checking", "balance": 4500.00}); 
