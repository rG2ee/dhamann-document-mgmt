STATISTIK_OUT    := absender_statistik.txt
DIRSTRUCTURE_OUT := directory_structure.txt

.PHONY: refresh-absendestatistik refresh-directory-structure

refresh-absendestatistik:
	uv run python src/email_regeln/absender_statistik.py | tee $(STATISTIK_OUT)
	@echo ""
	@echo "→ Gespeichert in $(STATISTIK_OUT)"

refresh-directory-structure:
	uv run python src/email_regeln/imap_connection.py | tee $(DIRSTRUCTURE_OUT)
	@echo ""
	@echo "→ Gespeichert in $(DIRSTRUCTURE_OUT)"
