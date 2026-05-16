STATISTIK_OUT    := absender_statistik.txt
DIRSTRUCTURE_OUT := directory_structure.txt
WORKTREE_DIR     := /home/user/alle-freelancer-rechnungen-worktrees

.PHONY: refresh-absendestatistik refresh-directory-structure refresh-all
.PHONY: worktree worktree-check-status worktree-remove

refresh-all: refresh-absendestatistik refresh-directory-structure

refresh-absendestatistik:
	uv run python src/email_regeln/absender_statistik.py | tee $(STATISTIK_OUT)
	@echo ""
	@echo "→ Gespeichert in $(STATISTIK_OUT)"

refresh-directory-structure:
	uv run python src/email_regeln/imap_connection.py | tee $(DIRSTRUCTURE_OUT)
	@echo ""
	@echo "→ Gespeichert in $(DIRSTRUCTURE_OUT)"

worktree-check-status:
	@echo "=== Worktree Status ==="
	@for wt in $$(git worktree list --porcelain | grep '^worktree ' | sed 's/^worktree //'); do \
		branch=$$(git -C "$$wt" rev-parse --abbrev-ref HEAD 2>/dev/null); \
		if [ "$$branch" = "HEAD" ]; then continue; fi; \
		ahead=$$(git log master.."$$branch" --oneline 2>/dev/null | wc -l | tr -d ' '); \
		dirty=$$(git -C "$$wt" status --porcelain 2>/dev/null | wc -l | tr -d ' '); \
		if [ "$$ahead" -eq 0 ] && [ "$$dirty" -eq 0 ]; then \
			status="✓ gemergt & clean"; \
		elif [ "$$ahead" -eq 0 ]; then \
			status="⚠ gemergt, aber $$dirty uncommitted"; \
		else \
			status="✗ $$ahead commits nicht in master, $$dirty uncommitted"; \
		fi; \
		printf "%-50s %-20s %s\n" "$$wt" "[$$branch]" "$$status"; \
	done

worktree-remove:
ifndef branch
	$(error Usage: make worktree-remove branch=<branch_name>)
endif
	@ahead=$$(git log master..$(branch) --oneline 2>/dev/null | wc -l | tr -d ' '); \
	if [ "$$ahead" -gt 0 ]; then \
		echo "✗ Branch $(branch) hat $$ahead commits nicht in master. Abbruch."; \
		exit 1; \
	fi
	git worktree remove $(WORKTREE_DIR)/$(branch)
	git branch -d $(branch)

worktree:
ifndef branch
	$(error Usage: make worktree branch=<branch_name>)
endif
	@mkdir -p $(WORKTREE_DIR)
	git worktree add -b $(branch) $(WORKTREE_DIR)/$(branch)
	direnv allow $(WORKTREE_DIR)/$(branch)
