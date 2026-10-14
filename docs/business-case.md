# Business Case: Flash Card

## Metadata
| Key | Value |
| --- | --- |
| ID | BC-001 |
| CrossReference | [SA-001] |
| Language | en |
| Domain | it |

## Version History
| Date | Status | Author | Reviewer | Change | Commit |
| --- | --- | --- | --- | --- | --- |
| 2026-10-14 | Accepted | Jens Tirsvad Nielsen | AI as stand-in for S01 | Initial version | pending |

---

## Executive Summary

The Day 31 assignment of Udemy's *100 Days of Code: The Complete Python Pro Bootcamp* asks the course participant to build a flash card program that helps learn the most frequent words of a foreign language. The program shows a word in the target language, flips the card after three seconds to show its translation, and keeps only the words the learner does not yet know. This project delivers that program for a Malay to Danish word list, built from the four assignment steps (user interface, new flash cards, flipping the cards, saving progress) and extended with spoken Malay words. It is delivered as readable, tested, documented code that other course participants can run and compare with their own solution.

## Methodological and Standards Foundation

- Method: the SQA and QC framework of this repository (plan first, review every artifact against its QC checklist, one pull request per milestone); Larman, *Applying UML and Patterns*, for the use of layers and the presentation pattern.
- Architecture: clean architecture (domain, application, infrastructure, presentation) with MVVM for the user interface, as the `clean-architecture` skill sets out.
- Quality standard: ISO/IEC 25010:2023 product quality characteristics, as every QC criterion is tagged.
- Code: PEP 8, PEP 257 and type hints; Python 3.13 or later; Doxygen comments; `pytest` for tests.

## Problem Statement

- A learner who memorises vocabulary from a plain list has no way to see which words are already known, so time is spent on words that are mastered.
- The course assignment gives a step-by-step description, not a finished and tested reference that a participant can read, run and compare against.
- The supplied starting data is French to English. The Product Owner learns Malay and reads Danish, so the program must work with a Malay to Danish list and pronounce the Malay word.

## Business Opportunity

A small, well-structured reference solution gives the Product Owner a language learning tool for daily use, shows how clean architecture applies to a Tkinter program, and gives other course participants and repository visitors an example to learn from.

## Objectives

1. Deliver the four assignment steps as working behaviour: the window with a card and two buttons; a random card per button press; a flip to the translation after 3000 ms; and persistence of the unknown words in `words_to_learn.csv`.
2. Use the Malay to Danish frequency word list (`data/ms-da.csv`, 1000 words) instead of the French to English list, and speak the Malay word through text to speech without making that a requirement of the core program.
3. Keep the core program free of third-party runtime dependencies.
4. Provide a repository others can use: README, wiki in English, Danish and Bahasa Malaysia, screenshots, a repository description and topics.
5. Keep track of the work step by step, with one reviewed milestone and one pull request per step.

## Scope

### In Scope

- Python 3.13 or later Tkinter program with the assignment's function names (`next_card`, `flip_card`, `is_known`).
- Reading the Malay to Danish list from `data/ms-da.csv` (semicolon separated, header `ms;da`).
- Saving the words still to learn to `data/words_to_learn.csv` and using that file on the next start.
- Optional spoken Malay word (text to speech) as an extra that can be installed.
- `pyproject.toml`, `.gitignore`, `Doxyfile`, virtual environment instructions, `pytest` tests and `constants.py`.
- README from the framework template, screenshots, and a wiki in English, Danish and Bahasa Malaysia.
- Repository description and topics on the git host.
- The framework documents of the baseline: Business Case, Stakeholder Analysis, Project Plan, milestones, review records and traceability matrix.

### Out of Scope

- Other languages: the user interface labels are Malay and Danish only; another word list works by changing the data file but is not delivered.
- Spaced repetition scheduling, statistics, accounts, cloud synchronisation and mobile apps.
- Packaging for distribution on PyPI or as an installer.
- Redistribution of the course's own image files; the card and button images are generated for this project.
- A translation quality review of the word list.

## Expected Benefits

### Tangible Benefits

- A working flash card program for 1000 Malay words with progress that survives a restart.
- A test suite that protects the behaviour of every assignment step.
- A repository other participants can run in five commands or fewer.

### Intangible Benefits

- A worked example of clean architecture and MVVM in a small Tkinter program.
- Practice of the plan-first workflow with reviews and pull requests per step.
- Learning material in three languages for readers of the wiki.

## Strategic Alignment

The project supports the Product Owner's goal of completing the 100 Days of Code course with understood, well-documented solutions, and the goal of a public repository that shows disciplined engineering practice to its viewers.

## Success Criteria

| # | Criterion | Target | Measure |
| --- | --- | --- | --- |
| 1 | Assignment steps delivered | 4 of 4 steps work as described in the assignment | Acceptance checks listed in each step's milestone are all passed |
| 2 | Tests | `pytest` exits with 0 and every behaviour of steps 1 to 4 has at least one test | `pytest` run on a clean `.venv`, and the milestone's task list |
| 3 | Runtime dependencies of the core program | 0 third-party packages | `dependencies` in `pyproject.toml` is empty; speech is an optional extra |
| 4 | Time to run for a newcomer | 5 commands or fewer from clone to running window | Command count in the README's Setup and Run sections |
| 5 | Wiki coverage | 3 languages (en, da, ms) with the same page set | File list of `docs/wiki/` |
| 6 | Repository presentation | A description and at least 5 topics are set on the repository | Read back from the git host API |
| 7 | Review coverage | Every artifact and every milestone's code has an `RC-*` record with verdict Go | `docs/sqa/reviews/` and the Traceability Matrix |
| 8 | Delivery window | Everything merged by 2026-10-21 | Date of the last merged pull request |

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Text to speech needs network access and an audio player that may not work on every machine | Spoken word missing for some users | Speech is an optional extra behind a port; the program starts and works without it, and a failure is logged, not raised |
| The `playsound` package is unmaintained and fails on some Python versions | Install of the extra fails | Pin the version known to work (1.2.2), keep the player behind a port so it can be replaced |
| Tkinter cannot be tested without a display on a build machine | Presentation code untested in CI | The view model holds the behaviour and is tested without Tkinter; the view test skips when no display exists |
| The word list has translation errors (machine translated) | Learner learns a wrong meaning | Out of scope for this project; the README says the list is machine translated and may be edited |
| Course images are copyrighted | Redistribution not allowed in a public repository | Images are generated by a script in this repository |

## Assumptions

- S01 is the Product Owner, the developer and the reviewer; no other person reviews, so the AI acts as stand-in reviewer in autonomous mode and the review records say so.
- S01 can reach S02 and S03 only through the public repository; no interviews are held.
- A display and Tkinter are available on the machine where the program runs.
- Network access is available when the optional speech extra is used.
- The git host `git.tirsystem.com` is used for the repository, the wiki and the pull requests.

## Constraints

- Python 3.13 or later, with a virtual environment in `.venv`.
- The folder structure is `src/`, `tests/` and `docs/`.
- Constants are defined in `constants.py`.
- The assignment's function names are kept so that participants can compare solutions.
- The Product Owner's language is English and the domain is IT; the wiki is in English, Danish and Bahasa Malaysia.
- Delivery by 2026-10-21 (self-set, one week).

## Cost–Benefit Assessment

| Costs | Benefits |
| --- | --- |
| About one working week of the Product Owner's time to review the plan and the result | A reusable learning tool and a reference solution. Qualitative on purpose: no revenue is expected, so a quantitative return does not apply; the benefit is learning and portfolio value |
| No licence or hosting cost; the git host and Python are already available | Documentation and tests reusable for the next course day |
| Maintenance of the optional speech extra | An example of clean architecture for S02 and S03 |

## Stakeholders

| Stakeholder ID (SA) | Interest in this project |
| --- | --- |
| S01 | Owns the product, builds it and reviews it; wants a working tool and a learning record |
| S02 | Wants readable, runnable code with the assignment's function names and run instructions |
| S03 | Wants a clear repository description, topics and README, and no runtime dependencies |

## Recommendation

Proceed — the scope is small, the risks are mitigated, and the result serves the Product Owner and two groups of readers at no cost beyond the Product Owner's time.

---

[SA-001]: ./stakeholder-analysis.md
