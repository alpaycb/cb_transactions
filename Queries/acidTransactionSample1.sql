START TRANSACTION;
UPDATE bankAccounts.clientScope.accountingInfo SET balance = balance + 100 WHERE accountNumber = "123456789";
SELECT accountNumber, balance  from bankAccounts.clientScope.accountingInfo WHERE accountNumber = "123456789";
UPDATE bankAccounts.clientScope.accountingInfo SET balance = balance - 100 WHERE accountNumber = "987654321";
SELECT accountNumber, balance FROM bankAccounts.clientScope.accountingInfo WHERE accountNumber = "987654321";
COMMIT TRANSACTION;
