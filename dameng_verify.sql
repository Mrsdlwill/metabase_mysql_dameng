SELECT 'dmma_suppliers' AS table_name, COUNT(*) AS cnt FROM SYSDBA.dmma_suppliers
UNION ALL
SELECT 'dmma_materials', COUNT(*) FROM SYSDBA.dmma_materials
UNION ALL
SELECT 'dmma_standards', COUNT(*) FROM SYSDBA.dmma_standards
UNION ALL
SELECT 'dmma_documents', COUNT(*) FROM SYSDBA.dmma_documents;
