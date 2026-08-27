# Copilot Instructions for identificaprocesso

## Overview

This repository contains a utility for identifying Brazilian court proceedings using the CNJ (Conselho Nacional de Justiça) standard format. The tool validates and parses process numbers according to Resolution 65/2008 and returns the corresponding court and tribunal information.

## Project Structure

- **consulta_juizo_cnj.py** - Main Python script that provides the core functionality
- **matriz_codigos_cnj.json** - Data file containing all court hierarchies and unit codes

## Running the Application

### Basic Usage
```bash
# Interactive mode - prompts for a process number
python3 consulta_juizo_cnj.py

# Direct mode - pass process number as argument
python3 consulta_juizo_cnj.py 0010507-38.2021.5.18.0008
```

### Expected Output
Returns a single line: `Juízo: [Unit Name] — [Court Name]`

## Process Number Format

The tool expects CNJ format: `NNNNNNN-DD.AAAA.J.TR.OOOO`

- **NNNNNNN** - Sequential process number
- **DD** - Check digit
- **AAAA** - Year of filing
- **J** - Justice system code (1 digit)
- **TR** - Court code (2 digits)
- **OOOO** - Court unit code (4 digits)

## Code Architecture

### Key Components

1. **MAPA_JUSTICA** - Maps justice system codes (J) to their JSON keys and display names
   - `1, 7, 9` = Federal Justice
   - `2` = State Military Justice
   - `3` = Federal Military Justice
   - `4, 5` = Labor Justice
   - `6` = Electoral Justice
   - `8` = State Justice

2. **Parsing Pipeline**
   - Regex validation (`REGEX_CNJ`) against the standard format
   - Field extraction into components
   - Hierarchical lookup: Justice system → Tribunal → Unit of origin
   - Error handling with descriptive messages

3. **Data Structure** (matriz_codigos_cnj.json)
   ```
   {
     "[justice_key]": {
       "descricao": "[description]",
       "tribunais": {
         "[tribunal_code]": {
           "nome_tribunal": "[tribunal name]",
           "unidades_origem_oooo": {
             "[unit_code]": "[unit name]",
             ...
           }
         }
       }
     }
   }
   ```

## Key Conventions

### Error Handling
- Raises `ValueError` with context-specific messages for invalid inputs:
  - Invalid format
  - Unrecognized justice code
  - Missing tribunal in matrix
  - Missing unit code in tribunal

- Raises `FileNotFoundError` if matrix file is missing

### File Encoding
All files use UTF-8 encoding (Portuguese characters)

### Code Style
- Scripts are self-documenting with clear function docstrings
- Configuration constants are defined at module level (MATRIZ_PATH, REGEX_CNJ, MAPA_JUSTICA)
- Main logic separated into pure functions for testability

## Testing

No automated test suite currently exists. To manually validate:

```bash
# Valid process number (should return a court name)
python3 consulta_juizo_cnj.py 0010507-38.2021.5.18.0008

# Invalid format (should raise error)
python3 consulta_juizo_cnj.py invalid-process

# Missing unit code (should raise error with informative message)
python3 consulta_juizo_cnj.py 0000000-00.0000.5.18.9999
```

## Adding New Courts or Units

To expand the matrix:

1. Update `matriz_codigos_cnj.json` with new tribunal or unit codes
2. Follow the existing hierarchy structure exactly
3. Ensure all strings use UTF-8 and proper Portuguese names
4. No code changes needed - the lookup logic handles new entries automatically

## Dependencies

- Python 3.x standard library only (json, re, sys, pathlib)
- No external packages required
