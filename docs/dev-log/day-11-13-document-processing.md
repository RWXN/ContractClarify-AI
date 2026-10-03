# Day 11-13 Document Upload, Logging, and Test sprint

## completed

Current chunking is character-based. A future improvement is semantic or sentence-aware chunking.
Current PDF extraction supports text-based PDFs. Scanned image PDFs are not supported yet.

- Added PDF/TXT text extraction, cleaning, and chunking services 
- Added the document_chunks table and DocumentChunk model featuring a pgvector-ready embedding field.
- Integrated automatic document processing into the upload flow, updating statuses and saving text previews.
- Added Alembic database migration and a new endpoint to inspect document chunks.