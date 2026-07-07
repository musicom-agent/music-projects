# Flat.io API Integration Notes

## Overview
Flat.io provides a REST API that is superior to BandLab for headless agent control because it allows programmatic score creation, retrieval, and editing.

## Technical Details

### Authentication
Use a **Personal Access Token** (Bearer Token) in the `Authorization` header.
- Endpoint Base: `https://api.flat.io/v2/`

### File Handling
- **Preferred Format**: MusicXML. Preserves more metadata (lyrics, layout, articulations) than MIDI.
- **Conversion**: Use `music21` to convert local MIDI compositions to MusicXML before uploading.

### Python Client
- `pip install flat_api`
- Follows Swagger/OpenAPI spec structure.

### Key Endpoints
- `POST /scores`: Create a new score or upload a file.
- `GET /scores/{id}/revisions/{id}/exports/{format}`: Get PNG/PDF/MP3/MIDI.

## Workflow Example (Agent Role)
1. Compose melody in `music21`.
2. Push to GitHub repo.
3. Call Flat.io `POST /scores` with the MusicXML stream.
4. Deliver the Flat.io Web URL to the user for manual notation tweaks.
