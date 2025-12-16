# Development Plan: diag-agent (main branch)

*Generated on 2025-12-15 by Vibe Feature MCP*
*Workflow: [tdd](https://mrsimpson.github.io/responsible-vibe-mcp/workflows/tdd)*

## Goal
Implementierung von diag-agent: Ein LLM-Agent zur autonomen Generierung von Software-Architektur-Diagrammen mit automatischer Syntax-Validierung und Design-Feedback über Kroki-Integration.

## Explore

### Phase Entrance Criteria:
- [x] Orchestrator Cycle 2 abgeschlossen (LLMClient-Integration)
- [x] KrokiClient vorhanden (render_diagram mit Error-Handling)
- [x] Runtime View Scenario 2 dokumentiert (Orch → Validator → Error → LLM fix)
- [x] Bestehende Tests verstanden (3 Orchestrator-Tests, 2 Kroki-Tests)

### Tasks
- [x] **Orchestrator (Zyklus 3):** KrokiClient-Integration analysieren
- [x] KrokiClient API verstehen: render_diagram(source, type, format) → bytes or KrokiRenderError
- [x] Error-Message Format: "Kroki rendering failed for diagram type '{type}': HTTP {status} - {text}"
- [x] Runtime View Scenario 2 studieren: Validation-Loop mit LLM-Retry
- [x] MVP-Scope definieren: Validation ohne Analyzer (nur Syntax, kein Design)
- [x] Test-Strategie: Success-Case (LLM → Kroki ✅) + Error-Case (LLM → Kroki ❌ → Retry)

### Completed
- [x] KrokiClient-API: render_diagram() wirft KrokiRenderError bei Syntax-Error ✓
- [x] Error enthält: Status Code + Response Text (Kroki Error-Message)
- [x] Runtime View: Orch → Validator → Error → LLM fix(source, error) → Validator
- [x] MVP ohne separaten Validator: KrokiClient direkt im Orchestrator
- [x] 2 Test-Szenarien: (1) Success path, (2) Error → Retry → Success
- [x] Dependencies: KrokiClient ✓, LLMClient ✓, beide mit Error-Handling

## Red

### Phase Entrance Criteria:
- [x] Exploration ist abgeschlossen und Anforderungen sind dokumentiert
- [x] KrokiClient API verstanden (render_diagram + KrokiRenderError)
- [x] Test-Strategie definiert (2 Tests: Success + Error-Retry)
- [x] Es ist klar, welche Funktionalität als nächstes implementiert werden soll

### Tasks
- [x] **Orchestrator (Zyklus 3):** Tests für KrokiClient-Validation schreiben
- [x] Test 1: `test_orchestrator_validates_with_kroki_success`
- [x] Test validiert: KrokiClient.render_diagram() Call für Syntax-Check
- [x] Test validiert: Success-Path (1 Iteration, kein Retry)
- [x] Test 2: `test_orchestrator_retries_on_kroki_validation_error`
- [x] Test validiert: Error → Retry mit Error-Message im Prompt
- [x] Test validiert: 2 Iterationen, 2. erfolgreich
- [x] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 2 Tests in tests/unit/test_orchestrator.py hinzugefügt
- [x] Test 1: Success-Path (LLM → Kroki ✅ → Done)
- [x] Test 2: Error-Retry (LLM → Kroki ❌ → LLM fix → Kroki ✅)
- [x] Mocks: LLMClient + KrokiClient (wie in Cycle 1+2)
- [x] Bereit für Test-Ausführung (erwarte Fehler: KrokiClient nicht importiert)

## Green

### Phase Entrance Criteria:
- [x] 2 Tests geschrieben und schlagen fehl (RED)
- [x] Tests schlagen aus dem richtigen Grund fehl (KrokiClient nicht importiert)
- [x] Tests validieren erwartete Funktionalität (Validation + Retry)
- [x] Test-Typ: Unit-Tests mit Mocks (wie Cycle 1+2)

### Tasks
- [x] **Orchestrator (Zyklus 3):** KrokiClient-Integration implementieren
- [x] KrokiClient + KrokiRenderError import hinzufügen
- [x] KrokiClient im __init__ instantiieren (mit settings.kroki_local_url)
- [x] render_diagram() im Iteration-Loop aufrufen
- [x] try/except für KrokiRenderError implementieren
- [x] Refinement-Prompt bei Error bauen (enthält error + previous source)
- [x] Bei Success: break aus Loop
- [x] Alte Tests anpassen: KrokiClient mocken + kroki_local_url hinzufügen
- [x] Alle Tests ausführen und grün machen

### Completed
- [x] KrokiClient + KrokiRenderError importiert ✅
- [x] self.kroki_client = KrokiClient(settings.kroki_local_url) in __init__ ✅
- [x] Validation-Loop implementiert: try { render_diagram() } catch { refinement } ✅
- [x] Refinement-Prompt: "Fix the following {type} diagram. Previous attempt had this error: {error}" ✅
- [x] Alte Tests gefixt: KrokiClient-Mock + kroki_local_url hinzugefügt ✅
- [x] 5 Tests passed! ✅ (92% Coverage für Orchestrator)

## Refactor

### Phase Entrance Criteria:
- [x] Der Test ist grün (PASS)
- [x] Implementation ist vollständig und funktionsfähig
- [x] Keine Hacks oder Shortcuts (hardcoded values, etc.)
- [x] Die Lösung adressiert das eigentliche Problem

### Tasks
- [x] **Orchestrator (Zyklus 3):** Code Review durchführen
- [x] Docstrings vollständig ✓
- [x] Type hints geprüft: KrokiClient + KrokiRenderError imports korrekt ✓
- [x] Error-Handling validiert: try/except sauber, validation_error tracking ✓
- [x] Refinement-Prompt Format: Klar und vollständig (error + description + previous source) ✓
- [x] Potentielle Refactorings geprüft: Prompt extraction → YAGNI (nur 4 Zeilen) ✓
- [x] Pattern-Konsistenz: Analog zu LLMClient-Integration ✓
- [x] Keine Refactorings nötig - Code ist clean

### Completed
- [x] Code Review durchgeführt: Keine Änderungen nötig ✅
- [x] Pattern konsistent (Dependency Injection, Error-Handling mit try/except)
- [x] Docstrings vollständig, Type hints angemessen
- [x] Tests passed ✅ (92% Coverage für Orchestrator)
- [x] Orchestrator Zyklus 3 abgeschlossen ✅ (KrokiClient Validation-Loop)

## Explore (Cycle 4: File Output)

### Phase Entrance Criteria:
- [x] Orchestrator Cycle 3 abgeschlossen (Validation-Loop funktioniert)
- [x] Diagram Source wird generiert und validiert
- [x] CLI ruft orchestrator.execute() auf und erwartet output_path
- [x] Aktuell: Kein File-Writing implementiert

### Tasks
- [x] **Orchestrator (Zyklus 4):** File Output Strategie analysieren
- [x] Aktueller Zustand verstehen: output_path hardcoded, keine Files geschrieben
- [x] Output-Format-Parsing: `"png,svg,source"` → multiple files
- [x] Kroki OutputFormat analysieren: png, svg, pdf, jpeg
- [x] Source-Extension-Mapping: plantuml → .puml, mermaid → .mmd, etc.
- [x] Directory-Creation-Strategie: os.makedirs(output_dir, exist_ok=True)
- [x] MVP-Scope definieren: Alle Formate + Multi-File-Support

### Completed
- [x] CLI erwartet: result['output_path'] (single path) ✓
- [x] Orchestrator nimmt: output_dir + output_formats, nutzt sie aber nicht ✓
- [x] Output-Formate: png/svg/pdf/jpeg via Kroki, source via Text-Write ✓
- [x] File Naming: `diagram.{ext}` (YAGNI - kein Name-Generation) ✓
- [x] Implementation Location: In Orchestrator.execute() nach Success ✓
- [x] Return Strategy: Primary path (erstes Format in Liste) ✓
- [x] Source Extension Map: .puml (plantuml), .mmd (mermaid), default .{type} ✓

## Red (Cycle 4: File Output)

### Phase Entrance Criteria:
- [x] EXPLORE abgeschlossen - File Output Strategie definiert
- [x] Test-Typ entschieden: Unit-Tests mit tmpdir (echte Files, Mocks für Clients)
- [x] Test-Szenarien identifiziert: Single format, Multiple formats, Source extensions

### Tasks
- [x] **Orchestrator (Zyklus 4):** Tests für File Output schreiben
- [x] Test 1: `test_orchestrator_writes_single_format_file` (PNG only)
- [x] Test validiert: Directory creation, PNG file writing, correct bytes, output_path
- [x] Test 2: `test_orchestrator_writes_multiple_format_files` (png,svg,source)
- [x] Test validiert: 3 files written, KrokiClient calls for PNG+SVG, .puml extension
- [x] Test 3: `test_orchestrator_uses_correct_source_extension` (Mermaid → .mmd)
- [x] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 3 Tests in tests/unit/test_orchestrator.py hinzugefügt ✅
- [x] Test 1: Single format (PNG) - Directory + File creation
- [x] Test 2: Multiple formats - 3 Files (png, svg, source.puml)
- [x] Test 3: Extension mapping - Mermaid (.mmd)
- [x] Pattern: tmpdir fixture + Mocks für LLMClient + KrokiClient
- [x] Alle 3 Tests schlagen fehl (erwartete Fehler: Files nicht erstellt) ✅

## Green (Cycle 4: File Output)

### Phase Entrance Criteria:
- [x] RED-Phase abgeschlossen - 3 Tests schlagen fehl
- [x] Tests schlagen aus dem richtigen Grund fehl (Files nicht erstellt)
- [x] Implementierungs-Strategie klar (Directory creation + Format-Loop + Extension-Mapping)

### Tasks
- [x] **Orchestrator (Zyklus 4):** File Output implementieren
- [x] Imports hinzufügen: os, Path (pathlib)
- [x] Directory creation: os.makedirs(output_dir, exist_ok=True)
- [x] output_formats parsen: split(",") + strip()
- [x] Loop über Formate: source → write_text(), andere → render + write_bytes()
- [x] Helper-Methode: _get_source_extension() mit Extension-Map
- [x] primary_output_path tracking (erstes Format)
- [x] Alte Tests fixen: output_formats="png" + side_effect erweitern
- [x] Alle Tests ausführen und grün machen

### Completed
- [x] Imports: os, Path hinzugefügt ✅
- [x] File-Writing-Logic nach Iteration-Loop implementiert ✅
- [x] Directory creation mit exist_ok=True ✅
- [x] Format-Loop: source (write_text) + Kroki-Formate (write_bytes) ✅
- [x] Extension-Mapping: plantuml → .puml, mermaid → .mmd, default → .{type} ✅
- [x] primary_output_path = erstes Format ✅
- [x] 2 alte Tests gefixt (output_formats + side_effect) ✅
- [x] Alle 8 Tests GRÜN! ✅ (95% Coverage für Orchestrator)

## Refactor (Cycle 4: File Output)

### Phase Entrance Criteria:
- [x] Alle Tests grün (8 passed)
- [x] Implementation vollständig und funktionsfähig
- [x] Keine Hacks oder Shortcuts
- [x] Die Lösung adressiert das Problem

### Tasks
- [x] **Orchestrator (Zyklus 4):** Code Review durchführen
- [x] Docstrings vollständig ✓
- [x] Type hints geprüft ✓
- [x] Potentielle Refactorings evaluiert:
  - File-Writing extraction → NEIN (YAGNI, nur 20 Zeilen, 1x verwendet)
  - Prompt-Building extraction → NEIN (bereits Cycle 3 YAGNI)
  - Extension-Map als Konstante → NEIN (gut gekapselt)
  - os.makedirs → Path.mkdir → JA (Konsistenz mit Path-API)
- [x] Refactoring: Path.mkdir statt os.makedirs
- [x] Unused import entfernt: os
- [x] Tests nach Refactoring ausführen

### Completed
- [x] Code Review durchgeführt ✅
- [x] Refactoring: os.makedirs → Path.mkdir(parents=True, exist_ok=True) ✅
- [x] import os entfernt (nicht mehr benötigt) ✅
- [x] Alle Tests passed ✅ (95% Coverage für Orchestrator)
- [x] Orchestrator Zyklus 4 abgeschlossen ✅ (File Output komplett)
- [x] MVP Core 100% komplett! ✅

## Explore (KrokiClient Cycle 3: Content-Type Validation)

### Phase Entrance Criteria:
- [x] MVP Core komplett (Orchestrator File Output funktioniert)
- [x] Code Review von kroki-demo.py durchgeführt
- [x] Bug identifiziert: Content-Type nicht geprüft
- [x] Problem verstanden: Kroki gibt HTTP 200 + text/plain bei Syntax-Error

### Tasks
- [x] **KrokiClient (Zyklus 3):** Content-Type Validation analysieren
- [x] kroki-demo.py Pattern studieren: text/plain Check
- [x] Aktueller KrokiClient Code reviewen: Nur HTTP-Status geprüft
- [x] Bug dokumentieren: HTTP 200 + text/plain bei Syntax-Error nicht erkannt
- [x] MVP-Scope definieren: Content-Type Check nach raise_for_status()
- [x] Error-Message Strategy: response.text bei text/plain nutzen
- [x] Relevante vs irrelevante Patterns aus kroki-demo.py trennen

### Completed
- [x] kroki-demo.py analyzed ✓
- [x] Critical Bug: text/plain nicht geprüft (Kroki gibt HTTP 200 bei Error) ✓
- [x] Irrelevant für uns: URL-Encoding (zlib+base64), SVG-Type-Forcing ✓
- [x] Relevant: Content-Type Check, response.text für Error-Message ✓
- [x] Implementation Plan: Check nach raise_for_status(), raise wenn text/plain ✓

## Red (KrokiClient Cycle 3: Content-Type Validation)

### Phase Entrance Criteria:
- [x] EXPLORE abgeschlossen - Bug verstanden
- [x] Test-Strategie klar: Unit-Test mit Mock (HTTP 200 + text/plain)

### Tasks
- [x] **KrokiClient (Zyklus 3):** Test für Content-Type Validation schreiben
- [x] Test: test_render_diagram_text_plain_error
- [x] Mock: HTTP 200 + Content-Type: text/plain + error text im body
- [x] Assertion: KrokiRenderError raised trotz 200 status
- [x] Assertion: Error message enthält Kroki error text
- [x] Test ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] Test in tests/unit/test_kroki_client.py hinzugefügt ✅
- [x] Mock: HTTP 200, Content-Type: text/plain, error text im body ✅
- [x] Test schlägt fehl (erwarteter Fehler: DID NOT RAISE KrokiRenderError) ✅

## Green (KrokiClient Cycle 3: Content-Type Validation)

### Phase Entrance Criteria:
- [x] RED-Phase abgeschlossen - Test schlägt fehl
- [x] Test schlägt aus dem richtigen Grund fehl (DID NOT RAISE)
- [x] Implementation klar: Content-Type Check nach raise_for_status()

### Tasks
- [x] **KrokiClient (Zyklus 3):** Content-Type Validation implementieren
- [x] Content-Type Check nach raise_for_status() hinzufügen
- [x] response.headers.get('Content-Type', '') auslesen
- [x] Bei 'text/plain' → KrokiRenderError mit response.text
- [x] Alten Test fixen: mock_response.headers hinzufügen
- [x] Alle Tests ausführen und grün machen

### Completed
- [x] Content-Type Check nach raise_for_status() implementiert ✅
- [x] Bei text/plain: KrokiRenderError mit error message ✅
- [x] test_render_diagram_success gefixt (headers Mock hinzugefügt) ✅
- [x] Alle 3 KrokiClient-Tests GRÜN! ✅ (100% Coverage)
- [x] Alle 8 Orchestrator-Tests GRÜN! ✅ (95% Coverage)

## Refactor (KrokiClient Cycle 3: Content-Type Validation)

### Phase Entrance Criteria:
- [x] Alle Tests grün (3 KrokiClient + 8 Orchestrator)
- [x] Implementation vollständig und funktionsfähig
- [x] Keine Hacks oder Shortcuts
- [x] Die Lösung adressiert das Problem

### Tasks
- [x] **KrokiClient (Zyklus 3):** Code Review durchführen
- [x] Docstrings vollständig ✓
- [x] Type hints geprüft ✓
- [x] Potentielle Refactorings evaluiert:
  - Error-Message Duplication → NEIN (unterschiedliche Kontexte, YAGNI)
  - Content-Type Check extraction → NEIN (4 Zeilen, 1x verwendet, YAGNI)
  - Magic String 'text/plain' → NEIN (klar, selbsterklärend)
- [x] Keine Refactorings nötig - Code ist clean
- [x] kroki-demo.py löschen (alle Informationen extrahiert)

### Completed
- [x] Code Review durchgeführt ✅
- [x] Keine Refactorings nötig ✅
- [x] Alle Tests passed ✅ (100% Coverage für KrokiClient)
- [x] KrokiClient Zyklus 3 abgeschlossen ✅ (Content-Type Validation)
- [x] Bug gefixt: HTTP 200 + text/plain wird jetzt erkannt ✅
- [x] kroki-demo.py gelöscht ✅ (alle Learnings extrahiert)

## Explore (Settings Cycle 1: Kroki Mode Support)

### Phase Entrance Criteria:
- [x] E2E-Test erfolgreich mit Workaround (KROKI_LOCAL_URL=https://kroki.io)
- [x] Bug identifiziert: kroki_mode wird geladen aber ignoriert
- [x] Orchestrator nutzt immer kroki_local_url, egal was mode ist

### Tasks
- [x] **Settings (Zyklus 1):** Kroki Mode Bug analysieren
- [x] Aktueller Code: Orchestrator nutzt settings.kroki_local_url (Zeile 34)
- [x] Settings laden: kroki_mode, kroki_local_url (kein kroki_remote_url!)
- [x] .env.example definiert: DIAG_AGENT_KROKI_REMOTE_URL (wird nicht gelesen)
- [x] Bug-Root-Cause: Settings lesen kroki_remote_url nicht aus ENV
- [x] MVP-Scope definieren: kroki_url Property mit mode-basierter URL-Selektion

### Completed
- [x] Bug analysiert: kroki_mode und kroki_remote_url nicht implementiert ✓
- [x] Orchestrator.py:34 nutzt immer kroki_local_url ✓
- [x] Settings.py:48-51 laden nur kroki_local_url ✓
- [x] Solution Design: kroki_url @property basierend auf mode ✓
- [x] MVP: mode=local → local_url, mode=remote → remote_url ✓
- [x] auto-Mode deferred (YAGNI für E2E-Test) ✓

## Red (Settings Cycle 1: Kroki Mode Support)

### Phase Entrance Criteria:
- [x] EXPLORE abgeschlossen - Solution Design klar
- [x] Test-Strategie klar: Unit-Tests mit ENV mocks

### Tasks
- [x] **Settings (Zyklus 1):** Tests für kroki_url Property schreiben
- [x] Test 1: mode=local → returns kroki_local_url
- [x] Test 2: mode=remote → returns kroki_remote_url
- [x] Test 3: invalid mode → fallback to local_url
- [x] Tests in test_settings.py hinzugefügt
- [x] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 3 Tests in tests/unit/test_settings.py hinzugefügt ✅
- [x] Test Pattern: patch.dict(os.environ) wie existing tests ✅
- [x] Alle 3 Tests schlagen fehl (erwarteter Fehler: AttributeError kroki_url) ✅

## Green (Settings Cycle 1: Kroki Mode Support)

### Phase Entrance Criteria:
- [x] RED-Phase abgeschlossen - Tests schlagen fehl
- [x] Tests schlagen aus dem richtigen Grund fehl (AttributeError)
- [x] Implementation klar: kroki_remote_url + kroki_url @property

### Tasks
- [x] **Settings (Zyklus 1):** kroki_url Property implementieren
- [x] Settings.py: kroki_remote_url Attribut hinzufügen
- [x] __init__: kroki_remote_url aus ENV laden (DIAG_AGENT_KROKI_REMOTE_URL)
- [x] kroki_url @property implementieren: mode-basierte URL-Selektion
- [x] Orchestrator.py updaten: settings.kroki_url statt settings.kroki_local_url
- [x] Test-Fix: load_dotenv() mocken in test_load_settings_with_defaults
- [x] Alle Tests ausführen und grün machen

### Completed
- [x] kroki_remote_url Attribut + ENV loading ✅
- [x] kroki_url @property: remote → remote_url, local/invalid → local_url ✅
- [x] Orchestrator: KrokiClient(settings.kroki_url) ✅
- [x] Test-Fix: load_dotenv() gemockt ✅
- [x] Alle 6 Settings-Tests GRÜN! ✅ (100% Coverage)
- [x] Alle 8 Orchestrator-Tests GRÜN! ✅ (95% Coverage)

## Refactor (Settings Cycle 1: Kroki Mode Support)

### Phase Entrance Criteria:
- [x] Alle Tests grün (6 Settings + 8 Orchestrator)
- [x] Implementation vollständig und funktionsfähig
- [x] Bug fixed: kroki_mode wird jetzt respektiert

### Tasks
- [x] **Settings (Zyklus 1):** Code Review durchführen
- [x] Docstrings vollständig ✓
- [x] Type hints geprüft ✓
- [x] Potentielle Refactorings evaluiert:
  - kroki_url Logic extraction → NEIN (4 Zeilen, YAGNI)
  - Mode validation → NEIN (graceful fallback reicht)
  - Docstring improvements → Optional (bereits klar)
- [x] Keine Refactorings nötig - Code ist clean

### Completed
- [x] Code Review durchgeführt ✅
- [x] Keine Refactorings nötig ✅
- [x] Alle Tests passed ✅ (Settings 100%, Orchestrator 95%)
- [x] E2E-Test erfolgreich OHNE Workaround ✅ (mode=remote funktioniert korrekt)
- [x] Settings Zyklus 1 abgeschlossen ✅ (Kroki Mode Support)
- [x] Bug gefixt: DIAG_AGENT_KROKI_MODE=remote funktioniert jetzt ✅

## Explore (Design Analyzer Cycle 1: Vision-based Feedback)

### Phase Entrance Criteria:
- [x] Core features complete (Settings, KrokiClient, Orchestrator, LLMClient)
- [x] E2E test successful (syntax validation working)
- [x] Documentation reviewed (Runtime View, Building Block View, Concepts)
- [x] User requested design feedback feature ("ja")

### Tasks
- [ ] **Design Analyzer (Zyklus 1):** Vision-based feedback loop requirements analysieren
- [ ] Runtime View Scenario 1 verstehen: Orch → Analyzer → LLM vision
- [ ] Building Block View L2: Design Analyzer verantwortlichkeiten
- [ ] Concepts: validate_design config + graceful degradation verstehen
- [ ] LiteLLM Vision API research: Wie vision_analyze() implementieren
- [ ] MVP-Scope definieren: Welche Design-Kriterien evaluieren
- [ ] Test-Strategie: Unit-Tests für Analyzer + LLMClient vision_analyze()

### Completed
- [x] EXPLORE Phase abgeschlossen ✓
- [x] Design Analyzer requirements verstanden ✓
- [x] LiteLLM Vision API pattern recherchiert ✓
- [x] MVP-Scope definiert: LLMClient.vision_analyze() ✓
- [x] Test-Strategie klar: 2 Unit-Tests (success + error) ✓
- [x] Runtime View (Scenario 1) studiert ✓
  - Orch → Analyzer.analyze_design(png)
  - Analyzer → LLM.vision_analyze(png, criteria)
  - LLM returns design feedback (e.g., "Layout cramped, suggest vertical")
  - Feedback flows to Orchestrator → refinement prompt
- [x] Building Block View L2 (lines 116-120) ✓
  - Component: "Design Analyzer", "Vision-based feedback"
  - Only active if vision-capable LLM configured
  - Renders diagram to PNG → sends to LLM with evaluation prompt
  - Parses feedback (layout, clarity, C4 compliance, etc.)
- [x] Concepts (08_concepts.adoc) ✓
  - Config: llm.vision_enabled: true (line 48)
  - Config: agent.validate_design: true (line 61) - "Only if vision_enabled"
  - Graceful degradation (line 112): "No vision model: Skip design analysis"
  - Error handling (lines 93-95): Design Issues → feed back to LLM
  - Progress messages (lines 136-139): "📊 Analyzing design...", "⚠ Layout could be improved"
- [x] Solution Strategy (04_solution_strategy.adoc, line 30) ✓
  - Step 4: "Analyze (if vision available): Render image, LLM evaluates layout/design"
  - Feedback loop includes design refinement (step 5)
- [x] Current codebase status ✓
  - LLMClient: Only generate() implemented (text-only, no vision)
  - analyzer.py: Empty file (placeholder)
  - Settings: No validate_design or vision_enabled yet
  - .env.example line 19: DIAG_AGENT_VALIDATE_DESIGN=true (not loaded)
- [x] LiteLLM Vision API research ✓
  - API Pattern: Same completion() but messages.content is array
  - Text + Image: [{"type": "text", "text": "..."}, {"type": "image_url", "image_url": {"url": "..."}}]
  - Image formats: URL or base64 data URL ("data:image/png;base64,...")
  - Claude support: claude-3-7-sonnet-latest supports vision
  - Documentation: https://docs.litellm.ai/docs/completion/vision
- [x] MVP-Scope definition ✓
  - **Cycle 1 Focus**: LLMClient.vision_analyze() method
  - Input: PNG bytes (from Kroki), analysis prompt
  - Output: Design feedback string (or "approved")
  - Base64 encoding: Convert bytes → data URL
  - Design criteria (MVP): Layout quality, readability, spacing
  - Error handling: LLMGenerationError (reuse existing exception)
  - **Deferred**: Settings.validate_design, DesignAnalyzer component, Orchestrator integration
- [x] Test-Strategie definition ✓
  - **Test 1**: vision_analyze() with mock LiteLLM (success case)
  - Mock: litellm.completion returns design feedback message
  - Assert: Correct base64 encoding, proper message structure
  - **Test 2**: vision_analyze() error handling (API failure)
  - Mock: litellm.completion raises exception
  - Assert: Raises LLMGenerationError with context

## Red (Design Analyzer Cycle 1: Vision-based Feedback)

### Phase Entrance Criteria:
- [x] EXPLORE abgeschlossen - Requirements klar
- [x] LiteLLM Vision API pattern verstanden
- [x] MVP-Scope definiert: LLMClient.vision_analyze()
- [x] Test-Strategie klar: 2 Unit-Tests

### Tasks
- [ ] **LLMClient (Vision-Methode):** Tests für vision_analyze() schreiben
- [ ] Test 1: test_vision_analyze_design_feedback_success
- [ ] Test validiert: PNG bytes → base64 data URL conversion
- [ ] Test validiert: Messages array mit text + image_url structure
- [ ] Test validiert: Design feedback string returned
- [ ] Test 2: test_vision_analyze_api_error
- [ ] Test validiert: LiteLLM exception → LLMGenerationError
- [ ] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 2 Tests in tests/unit/test_llm_client.py hinzugefügt ✅
- [x] Test 1: test_vision_analyze_design_feedback_success ✅
  - Validates PNG bytes → base64 data URL conversion
  - Validates vision message structure (text + image_url array)
  - Validates design feedback extraction from LLM response
- [x] Test 2: test_vision_analyze_api_error ✅
  - Validates LiteLLM exception → LLMGenerationError
  - Validates error context includes model name
- [x] Tests ausgeführt - beide schlagen fehl ✅
- [x] Fehler ist korrekt: AttributeError: 'LLMClient' object has no attribute 'vision_analyze' ✅

## Green (Design Analyzer Cycle 1: Vision-based Feedback)

### Phase Entrance Criteria:
- [x] RED Phase abgeschlossen - 2 Tests schlagen fehl
- [x] Tests schlagen aus dem richtigen Grund fehl (AttributeError)
- [x] Tests validieren erwartete Funktionalität (Vision-Analyse)
- [x] Test-Typ: Unit-Tests mit Mocks (analog zu generate())

### Tasks
- [ ] **LLMClient (Vision-Methode):** vision_analyze() implementieren
- [ ] Import base64 module für encoding
- [ ] vision_analyze(image_bytes: bytes, prompt: str) -> str signature
- [ ] PNG bytes → base64 data URL conversion implementieren
- [ ] Vision message structure bauen: [text, image_url]
- [ ] litellm.completion() mit vision messages aufrufen
- [ ] Design feedback aus response.choices[0].message.content extrahieren
- [ ] try/except für LLMGenerationError (analog zu generate())
- [ ] Alle Tests ausführen und grün machen

### Completed
- [x] vision_analyze() method implementiert ✅
- [x] Import base64 module ✅
- [x] PNG bytes → base64 data URL conversion ✅
- [x] Vision message structure: [text, image_url] array ✅
- [x] litellm.completion() mit vision messages ✅
- [x] Design feedback extraction ✅
- [x] Error-Handling: try/except → LLMGenerationError ✅
- [x] Alle 3 Tests GRÜN! ✅
  - test_generate_diagram_source_success ✅ (alter Test)
  - test_vision_analyze_design_feedback_success ✅ (neu)
  - test_vision_analyze_api_error ✅ (neu)
- [x] LLMClient Coverage: 92% (24 statements, 2 missed) ✅

## Refactor (Design Analyzer Cycle 1: Vision-based Feedback)

### Phase Entrance Criteria:
- [x] Alle Tests grün (3 LLMClient tests)
- [x] Implementation vollständig und funktionsfähig
- [x] Vision-based analysis implementiert (vision_analyze)

### Tasks
- [ ] **LLMClient (Vision-Methode):** Code Review durchführen
- [ ] Docstrings vollständig prüfen
- [ ] Type hints geprüft
- [ ] Potentielle Refactorings evaluieren:
  - [ ] Code-Duplication: model string building (generate + vision_analyze)
  - [ ] Error-Handling pattern (generate + vision_analyze)
  - [ ] Base64 encoding extraction
- [ ] YAGNI-Prinzip anwenden
- [ ] Keine unnötigen Abstractions

### Completed
- [x] Code Review durchgeführt ✅
- [x] Docstrings vollständig ✓ (Args, Returns, Raises dokumentiert)
- [x] Type hints geprüft ✓ (image_bytes: bytes, prompt: str, returns: str)
- [x] Potentielle Refactorings evaluiert ✓:
  - Model string building duplication (2x) → NEIN (1 Zeile, klar, YAGNI)
  - Response extraction duplication (2x) → NEIN (1 Zeile, klar, YAGNI)
  - Error-Handling pattern duplication → NEIN (kontextspezifische Messages)
  - base64 import inside method → OK (lazy import für optionales Feature)
- [x] Keine Refactorings nötig - Code ist clean ✅
- [x] Pattern-Konsistenz: vision_analyze() folgt generate() Pattern ✅
- [x] Alle Tests passed ✅ (3/3 LLMClient tests)
- [x] Design Analyzer Cycle 1 abgeschlossen ✅ (Vision-Methode in LLMClient)
- [x] LLMClient Coverage: 92% ✅

## Explore (Orchestrator Cycle 5: Design Feedback Integration)

### Phase Entrance Criteria:
- [x] Design Analyzer Cycle 1 complete (LLMClient.vision_analyze implemented)
- [x] Vision-based analysis funktioniert (Unit-Tests grün)
- [x] User requested Orchestrator integration ("ja")

### Tasks
- [ ] **Orchestrator (Cycle 5):** Design Feedback Loop requirements analysieren
- [ ] Aktuelle Orchestrator.execute() Struktur verstehen
- [ ] Wo Design-Check einbauen (nach Syntax-Validierung)
- [ ] Settings.validate_design boolean hinzufügen (ENV: DIAG_AGENT_VALIDATE_DESIGN)
- [ ] Design-Refinement Prompt Pattern definieren
- [ ] Test-Strategie: Unit-Tests mit Mocks
- [ ] MVP-Scope definieren

### Completed
- [x] Orchestrator.execute() Struktur analysiert ✓
  - Iteration loop: while iterations_used < max_iterations
  - Prompt building: initial vs refinement (mit validation_error)
  - LLM generation: llm_client.generate(prompt)
  - Syntax validation: kroki_client.render_diagram() → PNG bytes
  - Bei Syntax-OK: break (Zeile 98) → HIER soll Design-Check rein!
  - Bei Syntax-Error: validation_error setzen, weiter iterieren
- [x] Settings.validate_design analysiert ✓
  - Aktuell nicht vorhanden in Settings
  - .env.example line 19: DIAG_AGENT_VALIDATE_DESIGN=true
  - Muss hinzugefügt werden: validate_design: bool
  - Default: false (graceful degradation wenn kein Vision-Model)
- [x] Design-Feedback-Pattern (Runtime View) ✓
  - Nach Syntax-OK: vision_analyze(png, criteria_prompt)
  - Feedback-Beispiele: "Layout cramped, suggest vertical" oder "Looks good"
  - Refinement prompt mit design_feedback
  - Approval-Detection: z.B. "approved", "looks good"
- [x] MVP-Scope definiert ✓
  - **Cycle 5 Focus**: Orchestrator Design-Feedback-Integration
  - Settings.validate_design boolean (default: false)
  - Design-Check nach Syntax-Validation (wenn validate_design=true)
  - PNG bytes von render_diagram() speichern
  - vision_analyze() mit criteria prompt aufrufen  
  - design_feedback tracking (analog zu validation_error)
  - Refinement-Prompt mit Design-Feedback
  - Einfache Approval-Detection (String-Check: "approved" in feedback.lower())
  - **Deferred**: DesignAnalyzer component (direkt LLMClient nutzen, YAGNI)
- [x] Test-Strategie definiert ✓
  - **Test 1**: Design-Check success (validate_design=true, feedback="approved")
  - Mock: render_diagram() returns PNG bytes
  - Mock: vision_analyze() returns "The design looks good and is approved"
  - Assert: 1 iteration, no refinement
  - **Test 2**: Design-Check refinement (validate_design=true, feedback → approved)
  - Mock: vision_analyze() iteration 1 returns improvement suggestions
  - Mock: vision_analyze() iteration 2 returns "approved"
  - Assert: 2 iterations, design feedback in refinement prompt
  - **Test 3**: Design-Check disabled (validate_design=false)
  - Assert: vision_analyze() NOT called, nur Syntax-Validation
  - Assert: Backwards-compatible (existing behavior preserved)

## Red (Orchestrator Cycle 5: Design Feedback Integration)

### Phase Entrance Criteria:
- [x] EXPLORE abgeschlossen - Requirements klar
- [x] MVP-Scope definiert
- [x] Test-Strategie klar: 3 Unit-Tests

### Tasks
- [ ] **Settings:** validate_design attribute hinzufügen (wird in Tests gemockt)
- [ ] **Orchestrator (Cycle 5):** Tests für Design-Feedback-Loop schreiben
- [ ] Test 1: test_orchestrator_design_approved_first_iteration
- [ ] Test 2: test_orchestrator_design_refinement_then_approved
- [ ] Test 3: test_orchestrator_design_check_disabled
- [ ] Tests ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] 3 Tests in test_orchestrator.py hinzugefügt ✅
- [x] Test 1: test_orchestrator_design_approved_first_iteration ✅
  - Validates: vision_analyze() called, design approved, 1 iteration
  - Fehler: vision_analyze() called 0 times (Design-Check nicht implementiert)
- [x] Test 2: test_orchestrator_design_refinement_then_approved ✅
  - Validates: 2 iterations, design feedback in refinement prompt
  - Fehler: 1 iteration statt 2 (Design-Refinement-Loop fehlt)
- [x] Test 3: test_orchestrator_design_check_disabled ✅
  - Validates: vision_analyze() NOT called when validate_design=false
  - Status: PASSED (backwards compatible - correct!)
- [x] Tests ausgeführt - 2 schlagen fehl, 1 passed ✅
- [x] Fehler sind korrekt: Design-Feedback-Integration fehlt ✅

## Green (Orchestrator Cycle 5: Design Feedback Integration)

### Phase Entrance Criteria:
- [x] RED Phase abgeschlossen - 2 Tests schlagen fehl
- [x] Tests schlagen aus dem richtigen Grund fehl
- [x] Test 3 passed (backwards compatible)

### Tasks
- [ ] **Settings:** validate_design boolean hinzufügen
- [ ] validate_design: bool attribute
- [ ] ENV loading: DIAG_AGENT_VALIDATE_DESIGN (default: false)
- [ ] **Orchestrator:** Design-Feedback-Loop implementieren
- [ ] design_feedback variable tracking (analog zu validation_error)
- [ ] PNG bytes speichern nach render_diagram()
- [ ] Design-Check nach Syntax-OK (wenn validate_design=true)
- [ ] vision_analyze() mit criteria prompt aufrufen
- [ ] Approval detection: "approved" in feedback.lower()
- [ ] Refinement-Prompt mit design_feedback
- [ ] Break wenn approved, sonst continue iteration
- [ ] Alte Tests anpassen (validate_design in mocks setzen)
- [ ] Alle Tests ausführen und grün machen

### Completed
- [x] Settings.validate_design implementiert ✅
  - validate_design: bool attribute hinzugefügt
  - _get_bool_env() helper method implementiert
  - ENV loading: DIAG_AGENT_VALIDATE_DESIGN (default: false)
- [x] Orchestrator Design-Feedback-Loop implementiert ✅
  - design_feedback variable tracking
  - PNG bytes capture von render_diagram()
  - Design-Check nach Syntax-OK (wenn validate_design=true)
  - vision_analyze() mit criteria prompt
  - Approval detection: "approved" in feedback.lower()
  - Refinement-Prompt mit design_feedback
  - Break wenn approved, sonst continue
- [x] Alte Tests angepasst (validate_design=False in 8 tests) ✅
- [x] Alle 11 Tests GRÜN! ✅ (100% pass rate)
- [x] Orchestrator Coverage: 95% (hoch von 80%) ✅

## Refactor (Orchestrator Cycle 5: Design Feedback Integration)

### Phase Entrance Criteria:
- [x] Alle Tests grün (11 Orchestrator tests)
- [x] Implementation vollständig und funktionsfähig
- [x] Design-Feedback-Loop implementiert

### Tasks
- [ ] **Orchestrator + Settings:** Code Review durchführen
- [ ] Docstrings vollständig prüfen
- [ ] Type hints geprüft
- [ ] Potentielle Refactorings evaluieren:
  - [ ] Prompt building logic (3 branches)
  - [ ] Design criteria prompt (hardcoded string)
  - [ ] Approval detection logic
  - [ ] Design validation extraction
- [ ] YAGNI-Prinzip anwenden

### Completed
- [x] Code Review durchgeführt ✅
- [x] Docstrings vollständig ✓
  - Settings._get_bool_env(): Complete (Args, Returns)
  - Orchestrator.execute(): Focused on API contract (accurate)
  - Inline comments clear (design validation flow)
- [x] Type hints geprüft ✓
  - Settings.validate_design: bool ✓
  - Settings._get_bool_env(key: str, default: bool) -> bool ✓
  - Orchestrator variables have implicit types (clear from usage)
- [x] Potentielle Refactorings evaluiert ✓:
  - Prompt building (3 branches) → NEIN (3 lines each, clear inline, YAGNI)
  - Design criteria prompt string → NEIN (used once, YAGNI)
  - Approval detection logic → NEIN (1 line, simple, clear)
  - Design validation extraction → NEIN (17 lines, tightly integrated in loop, extraction reduces clarity)
- [x] Keine Refactorings nötig - Code ist clean ✅
- [x] Pattern-Konsistenz: Design-Feedback analog zu Syntax-Error-Handling ✅
- [x] Alle Tests passed ✅ (11/11 Orchestrator tests)
- [x] Orchestrator Cycle 5 abgeschlossen ✅ (Design-Feedback-Integration)
- [x] Design Analyzer complete ✅ (LLMClient vision + Orchestrator integration)

## Key Decisions

### Architektur-Entscheidungen (aus ADRs)
- **ADR-001**: Bash-Tool mit `--help` ist primär, MCP optional → Context-Effizienz
- **ADR-002**: Agent iteriert selbständig mit eigenem LLM-Client → Autonomie
- **ADR-003**: Local-First (Kroki Fat-JAR), kroki.io nur mit Consent → Privacy
- **ADR-005**: LiteLLM für Provider-Abstraction → 100+ Modelle unterstützt
- **ADR-006**: Docker mit gebundeltem Kroki (Fat-JAR) → Einfache Installation
- **ADR-008**: Click als CLI Framework → Rich UX, LLM-kompatibel
- **ADR-009**: uv/uvx als Package Management (ACCEPTED) → 5-10x schneller, modern (PEP 723)

### Tech Stack
- **Python**: 3.10+ (bestehende Expertise)
- **Package Management**: uv/uvx (PEP 723, einzige empfohlene Methode)
- **CLI**: Click (intuitive commands, gute Help-Ausgabe)
- **LLM**: LiteLLM (Provider-agnostisch)
- **MCP**: FastMCP (Standard-Protokoll)
- **Rendering**: Kroki (20+ Diagramm-Typen)
- **Config**: python-dotenv, PyYAML
- **HTTP**: requests/httpx
- **Testing**: pytest (Unit- und Integrationstests)

### Qualitätsziele (Priorität)
1. **Context Efficiency**: < 3k tokens pro Diagramm-Request
2. **Ease of Installation**: < 2 Min bis zum ersten Diagramm (mit uvx)
3. **Privacy & Security**: Local-First, kein Remote ohne Consent
4. **Autonomy**: Agent iteriert ohne Parent-LLM Intervention
5. **Extensibility**: Alle Kroki-Typen, einfacher Provider-Wechsel

### Test-Strategie (RED-Phase)
- **Test-Typ**: Unit-Test mit HTTP-Mock (pytest + unittest.mock)
- **TDD-Zyklen**:
  - Zyklus 1: Happy-Path (`test_render_diagram_success`) - PlantUML → PNG
  - Zyklus 2: Error-Handling (`test_render_diagram_http_error`) - HTTP 500 → KrokiRenderError
- **Design**: Generisches Interface + Custom Exception für klare Error-Messages

## Notes

### ADR-009 Accepted (2025-12-15)
**Decision**: Vollständige Migration zu uv/uvx als einziges Package Management Tool
- README.md vollständig auf uv umgestellt (kein pip-Fallback mehr)
- Installation, Quick Start, Development, und Usage Examples zeigen nur noch uv/uvx
- Qualitätsziel "Ease of Installation" adressiert: uvx ermöglicht Zero-Install-Execution

### Config Management - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 1 TDD-Zyklus komplett (RED→GREEN→REFACTOR)
- ✅ Settings-Klasse mit ENV + .env Support
- ✅ Graceful Error-Handling für ungültige Integer-Werte
- ✅ 3 Tests, 100% Coverage
- ✅ Production-ready: python-dotenv, type-safe

**Implementiert:**
- 7 Config-Optionen (LLM, Kroki, Agent, Logging)
- ENV var precedence: ENV > .env > defaults
- Helper-Methode `_get_int_env()` für robuste Type Conversion

### CLI Basis - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 2 TDD-Zyklen komplett (RED→GREEN→REFACTOR)
- ✅ Zyklus 1: `--help` output mit Click framework
- ✅ Zyklus 2: `create` command mit Orchestrator + Settings integration
- ✅ 100% CLI Coverage, 2 Tests passing
- ✅ Refactoring: `type` → `diagram_type` (built-in override fix)

**Implementiert:**
- Click @click.group() mit version 0.1.0
- create command mit --type, --output, --format options
- Settings + Orchestrator integration
- Minimal Orchestrator-Stub für Tests

### LLM Client - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 1 TDD-Zyklus komplett (RED→GREEN→REFACTOR)

**EXPLORE-Erkenntnisse:**
- **ADR-005**: LiteLLM für Provider-Abstraction → 100+ Modelle
- **Building Block View L2**: LLM Client = LiteLLM wrapper mit retry + error handling
- **Runtime View**: `generate(prompt)` → Diagramm-Source, später `vision_analyze(png)`
- **Bestehende Patterns**: KrokiClient-Struktur als Template (Custom Exception + Client-Klasse)
- **Settings-Integration**: llm_provider + llm_model (bereits in Settings ✓)

**MVP-Scope (erster TDD-Zyklus):**
- ✅ Text-Generierung (keine Vision)
- ✅ LiteLLM-Integration mit completion()
- ✅ Settings-basierte Provider/Model-Konfiguration
- ✅ Error-Handling für LLM API Errors
- ⏸️ Vision-Modus (später)
- ⏸️ Retry-Logic (später)
- ⏸️ Token-Counting (später)

**Dependencies:**
- Settings ✓ (llm_provider, llm_model)
- litellm package (muss installiert werden)
- httpx (bereits für KrokiClient installiert)

**Design-Entscheidungen:**
- Analog zu KrokiClient: Custom Exception (LLMGenerationError) + Client-Klasse
- Main method: `generate(prompt: str) -> str`
- LiteLLM completion() API nutzen
- Settings für Provider/Model statt hardcoded values

### Orchestrator - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 3 TDD-Zyklen komplett (RED→GREEN→REFACTOR)
- ✅ Zyklus 1: Iteration-Loop mit max_iterations + max_time_seconds
- ✅ Zyklus 2: LLMClient-Integration für echte Generierung
- ✅ Zyklus 3: KrokiClient Validation-Loop mit Error-Retry
- ✅ 5 Tests, 92% Coverage
- ✅ stopped_reason Logic (max_iterations | max_time | success)

**Implementiert:**
- Iteration-Loop mit while iterations_used < max_iterations
- Zeit-Tracking mit time.time() (start + elapsed)
- Limits aus Settings (max_iterations=5, max_time_seconds=60)
- Metadata: iterations_used, elapsed_seconds, stopped_reason
- LLMClient-Integration: self.llm_client = LLMClient(settings)
- KrokiClient-Integration: self.kroki_client = KrokiClient(settings.kroki_local_url)
- Validation-Loop: try { render_diagram() } catch { refinement prompt }
- Refinement-Prompt: "Fix the following {type} diagram. Previous attempt had this error: {error}..."
- Autonome Iteration bis Syntax valid oder Limits erreicht

### KrokiClient - ABGESCHLOSSEN ✅ (2025-12-15)
**Status**: 2 TDD-Zyklen komplett (RED→GREEN→REFACTOR)
- ✅ Happy-Path: render_diagram() mit HTTP POST
- ✅ Error-Handling: KrokiRenderError mit Context
- ✅ 100% Test Coverage
- ✅ Production-ready: Clean Code, keine TODOs

### MVP-Strategie: Bottom-Up mit Kroki Client
**Erste Komponente: Kroki Client** (`src/diag_agent/kroki/client.py`) ✅
- Klare Schnittstelle: HTTP POST → Kroki → PNG/SVG Response
- Keine komplexen Abhängigkeiten
- Gut testbar (Unit + Integration mit Mock/Real Kroki)
- Foundation für Agent Core

**Nächste Schritte nach Kroki Client:**
1. Config Management (Settings laden)
2. CLI Basis (Click command für `create`)
3. LLM Client (LiteLLM wrapper)
4. Agent Core (Orchestrator mit Feedback-Loop)
5. MCP Server (optional)

### Projekt-Struktur (src-Layout)
```
diag-agent/
├── src/
│   └── diag_agent/
│       ├── __init__.py
│       ├── __main__.py         # Entry point: python -m diag_agent
│       ├── cli/                # Click CLI commands
│       │   ├── __init__.py
│       │   └── commands.py
│       ├── agent/              # Agent Core
│       │   ├── __init__.py
│       │   ├── orchestrator.py # Main feedback loop
│       │   ├── prompt_builder.py
│       │   ├── validator.py    # Syntax validation
│       │   ├── analyzer.py     # Design analysis (vision)
│       │   └── limiter.py      # Iteration/time limits
│       ├── llm/                # LLM Client
│       │   ├── __init__.py
│       │   └── client.py       # LiteLLM wrapper
│       ├── kroki/              # Kroki Manager
│       │   ├── __init__.py
│       │   ├── client.py       # HTTP client
│       │   └── manager.py      # Lifecycle, health checks
│       ├── config/             # Configuration
│       │   ├── __init__.py
│       │   └── settings.py     # Config precedence
│       ├── mcp/                # MCP Server (optional)
│       │   ├── __init__.py
│       │   └── server.py       # FastMCP implementation
│       └── utils/              # Utilities
│           ├── __init__.py
│           └── logging.py
├── tests/
│   ├── unit/
│   │   └── test_kroki_client.py
│   └── integration/
│       └── test_feedback_loop.py
├── pyproject.toml
├── README.md
└── .env.example
```

## Explore (LLMClient Cycle 2: Prompt Optimization)

### Phase Entrance Criteria:
- [x] E2E test successful (diagram generated)
- [x] Problem identified: LLM returns markdown code blocks + explanations
- [x] Quality goal violated: Context Efficiency (unnecessary tokens)
- [x] User confirmed to optimize prompt pattern

### Tasks
- [ ] **LLMClient (Cycle 2):** Analyze current prompt pattern
- [ ] Current behavior: LLM wraps diagram in ```plantuml ... ``` + adds explanation
- [ ] Kroki tolerance analyzed: Works but suboptimal (extra parsing overhead)
- [ ] Token waste quantified: ~200 extra tokens per diagram
- [ ] Best practices research: Prompt patterns for code-only output
- [ ] MVP-Scope: Clean diagram code output (no markdown, no explanation)
- [ ] Test strategy: E2E test validating output format

### Completed
- [x] Problem verstanden ✓
  - Current prompt: "Generate a {diagram_type} diagram: {description}"
  - No output format constraints → LLM adds markdown + explanations
  - Example waste: 485 chars total, ~200 chars markdown/explanation overhead
  - Violates Context Efficiency quality goal
- [x] Prompt-Pattern best practices recherchiert ✓
  - Best Practice 2025: Explicit output format constraints
  - Pattern: "Return only the {diagram_type} code. No markdown formatting. No explanations."
  - LiteLLM supports system messages for persistent instructions
  - Sources: [Prompt Engineering Guide](https://www.promptingguide.ai/prompts/coding), [Lakera Guide 2025](https://www.lakera.ai/blog/prompt-engineering-guide)
- [x] MVP-Scope definiert ✓
  - **Cycle 2 Focus**: Add system message to LLMClient.generate()
  - System message: Clear output format instructions
  - User message: Unchanged (diagram description)
  - Expected result: Clean diagram code (no ```, no explanations)
  - **Deferred**: Prompt templates, dynamic prompting
- [x] Test-Strategie klar ✓
  - **Approach**: Integration test (not full E2E - too slow for TDD)
  - Mock LiteLLM but validate prompt structure
  - Assert: messages array has system + user messages
  - Assert: system message contains output format constraints
  - Alternative: E2E validation test (after GREEN phase)

## Red (LLMClient Cycle 2: Prompt Optimization)

### Phase Entrance Criteria:
- [x] EXPLORE abgeschlossen - Problem und Lösung klar
- [x] MVP-Scope definiert: System message mit output constraints
- [x] Test-Strategie klar: Unit-Test für prompt structure

### Tasks
- [ ] **LLMClient (Cycle 2):** Test für System Message schreiben
- [ ] Test: test_generate_uses_system_message_for_output_format
- [ ] Mock LiteLLM completion()
- [ ] Assert: messages array hat 2 Einträge (system + user)
- [ ] Assert: system message enthält "only", "no markdown", "no explanation"
- [ ] Test ausführen und Fehlschlag verifizieren (RED)

### Completed
- [x] Test geschrieben ✓
  - test_generate_uses_system_message_for_output_format in test_llm_client.py
  - Validates: 2 messages (system + user), system constraints, user prompt
- [x] Test schlägt erwartungsgemäß fehl ✓
  - Error: assert 1 == 2 (only 1 message, expected 2)
  - Current: Only user message
  - Expected: System message + user message
  - RED phase confirmed ✅

## Green (LLMClient Cycle 2: Prompt Optimization)

### Phase Entrance Criteria:
- [x] RED-Phase abgeschlossen - Test schlägt fehl
- [x] Test schlägt aus dem richtigen Grund fehl (missing system message)
- [x] Implementation klar: Add system message to generate()

### Tasks
- [ ] **LLMClient (Cycle 2):** System message implementieren
- [ ] System message mit output format constraints formulieren
- [ ] messages array: [{"role": "system", ...}, {"role": "user", ...}]
- [ ] System content: "Return only the diagram code. No markdown formatting. No explanations."
- [ ] Alte Tests prüfen (sollten weiter grün sein)
- [ ] Neuer Test grün machen

### Completed
- [x] System message implementiert ✓
  - Added system message to LLMClient.generate()
  - Content: "Return only the diagram code. No markdown formatting. No explanations."
  - messages array: [{"role": "system", ...}, {"role": "user", ...}]
- [x] Alte Tests gefixt ✓
  - test_generate_diagram_source_success updated for new message structure
  - All integration preserved (Orchestrator tests still green)
- [x] Alle 4 LLMClient tests grün ✓
- [x] Alle 11 Orchestrator tests grün ✓
- [x] Coverage: LLMClient 92%, Orchestrator 95% ✓

## Refactor (LLMClient Cycle 2: Prompt Optimization)

### Phase Entrance Criteria:
- [x] Alle Tests grün (4 LLMClient + 11 Orchestrator)
- [x] System message implementiert
- [x] Implementation vollständig und funktionsfähig

### Tasks
- [x] **LLMClient (Cycle 2):** E2E-Validation durchführen
- [x] E2E-Test mit echtem LLM durchgeführt
- [x] Ergebnis analysiert: 37% Token-Savings (485 → 304 chars)
- [x] Problem: Markdown-Blöcke (```) noch vorhanden
- [x] Entscheidung: Post-Processing implementieren (robust)
- [ ] Test für Markdown-Stripping schreiben (RED)
- [ ] Post-Processing implementieren: Strip ``` blocks
- [ ] E2E-Test validieren: Clean output

### Completed
- [x] Test für Markdown-Stripping geschrieben (RED) ✓
  - test_generate_strips_markdown_code_blocks
  - Validates: ```plantuml ... ``` → clean code
- [x] Post-Processing implementiert (GREEN) ✓
  - _strip_markdown_code_blocks() helper method
  - Regex pattern: ^```[\w]*\n(.*?)\n```$
  - Strips code blocks with/without language specifier
  - Applied in generate() after LLM response
- [x] Alle 5 LLMClient tests grün ✓
- [x] Alle 11 Orchestrator tests grün ✓ (integration preserved)
- [x] E2E-Test validiert ✓
  - Clean output: 196 chars (no ```, no explanations)
  - **Total savings: 60% (485 → 196 chars)**
  - PNG/SVG generated correctly
- [x] Coverage: LLMClient 94%, Orchestrator 95% ✓
- [x] Cycle 2 abgeschlossen ✓ (Prompt Optimization)

## E2E Test: Design Feedback Loop Validation

### Test Results (2025-12-16)
- [x] **E2E-Test durchgeführt** mit validate_design=true
- [x] **Autonomer Design-Feedback-Loop funktioniert!** ✅
- [x] Test-Szenario: Komplexes Sequence-Diagramm (User Registration Flow)
- [x] **Ergebnis:**
  - **Iterations: 4** (Design-Refinement aktiv!)
  - **Time: 67.2s** (max_time_seconds=60 → Limit erreicht)
  - **Stopped: max_time** (nicht success - Loop würde weiterlaufen)
  - **Source: 1742 characters** (großes, detailliertes Diagramm)
  - **PNG: 870x2209 px, 101KB** (sehr gut lesbar)

### Design-Optimierungen durch Vision-LLM:
1. **Layout-Parameter:**
   - ParticipantPadding 50
   - BoxPadding 25
   - SequenceMessageAlign center
   - ResponseMessageBelowArrow true
2. **Spacing:** ||| zwischen Nachrichten (bessere Lesbarkeit)
3. **Phasen-Trennung:** == Registration Phase ==, == Email Verification Phase ==
4. **Lifecycle:** activate/deactivate für Teilnehmer
5. **Multi-line messages:** Klarere Beschreibungen mit \n

### Key Insights:
- ✅ Design-Feedback-Loop ist vollständig funktional
- ✅ Vision-LLM macht sinnvolle Layout-Verbesserungen
- ✅ Iteration-Loop stoppt korrekt bei max_time
- ⚠️ Time-Limit kann erreicht werden bevor "approved"
- ⚠️ Bei komplexen Diagrammen: Syntax-Fehler nach Design-Refinement möglich

### CLI Enhancement:
- [x] CLI zeigt jetzt: iterations_used, elapsed_seconds, stopped_reason
- [x] Bessere Transparenz über autonomen Prozess

## Open Backlog Items

### Documentation (Later)
- [ ] **README.md Update**: Vollständige Installation, Quick Start, Examples
- [ ] **User Manual**: Detaillierte Nutzungsanleitung (Features, Configuration, Workflows)
- [ ] **Tutorial**: Step-by-step Guide für erste Diagramme (PlantUML, Mermaid, C4)

### Features
- [ ] **MCP Server**: FastMCP implementation für Tool-Integration
- [ ] **Kroki Manager**: Local deployment mit Fat-JAR (ADR-003: Local-First)
- [ ] **LLMClient Extensions**: Retry-Logic, Token-Counting, Streaming
- [ ] **CLI Extensions**: Weitere Commands (validate, analyze, convert), Interactive mode
- [ ] **Testing**: Integration Tests, E2E Tests, Performance Tests
- [ ] **Utilities**: Structured Logging, Prompt-Template-Management

---
*This plan is maintained by the LLM. Tool responses provide guidance on which section to focus on and what tasks to work on.*
