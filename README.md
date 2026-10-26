# SD5913_assignment3_ThisMessage

**English** | [简体中文](README.zh-CN.md)

## This Message — How Would You Reply?

A Chinese-language command-line interactive story about a missed appointment, a rainy journey, and the things friends leave unsaid. Created for **SD5913 Assignment 3: An interactive experience**.

**The game is currently in Chinese.** This English README explains the concept, controls, setup, and implementation; it does not change the game's language.

## The experience

You were supposed to meet your friend Lin Yu at a bookshop at 19:30. At 19:42, you are still at home when a message arrives: “Did you forget our plans today?”

What starts as a reply becomes an evening of decisions: what to bring, how to travel, whether to explain a delay, and what to do when you discover why this meeting matters. You can also communicate a change of plan and continue the conversation remotely after the event.

The intended audience is Chinese-speaking readers who enjoy everyday, character-driven interactive fiction. The experience explores how words, practical actions, and attention affect a fictional conversation. It has no relationship score, real-time countdown, or single “correct” reply.

- **Four acts and 33 story scenes**, with **11–19 decisions** in a complete playthrough.
- **14 original ASCII illustrations**, including a phone, subway, rainy street, bookshop, café, and riverside bridge.
- **Items and remembered decisions** that change available choices and later dialogue.
- **Five ending themes across six ending nodes**; one theme has separate in-person and remote versions.
- Backtracking, restart, a journey log, and an inventory view.
- Runs locally with the Python standard library. No API calls, accounts, or paid services are required.

Reading time varies. You can take your time: nothing advances until you make a choice.

## Requirements

- Python **3.10 or later**; Python **3.13** was used for validation.
- A terminal with UTF-8 and a monospaced font that supports Chinese characters.
- [uv](https://docs.astral.sh/uv/getting-started/installation/) for the recommended setup, or an existing compatible Python installation.

There are **no third-party Python dependencies**. Initial installation of Python through uv requires internet access; after setup, the game works offline.

## Quick start

Clone the repository and enter its directory:

~~~powershell
git clone https://github.com/Seven39c5bb/SD5913_assignment3_ThisMessage.git
cd SD5913_assignment3_ThisMessage
~~~

Set up and run with uv:

~~~powershell
uv python install 3.13
uv sync --python 3.13 --locked
uv run --locked python main.py
~~~

Alternatively, with a compatible Python installation already available:

~~~powershell
python main.py
~~~

The commands above work from the directory containing this README and pyproject.toml. The dependency metadata and lockfile are included in the repository.

### Display and demonstration options

~~~powershell
# Automatically follow the first available choice at every step until an ending.
uv run --locked python main.py --demo

# Disable ANSI colors while keeping the ASCII illustrations.
uv run --locked python main.py --plain

# Hide illustrations for a compact view or a screen reader.
uv run --locked python main.py --no-art

# Produce a plain-text, noninteractive demonstration.
uv run --locked python main.py --demo --plain --no-art
~~~

A terminal at least **60 columns wide** is recommended. When an illustration cannot fit, the game displays its scene label instead of breaking the drawing across lines. If Chinese characters appear as boxes, choose a font that includes Chinese glyphs. Color is optional and is disabled for redirected output; the NO_COLOR environment variable is also supported.

## Controls

Type a number or command and press **Enter**.

| Input | Action |
| --- | --- |
| 1, 2, or 3 | Select the corresponding reply or action currently shown |
| b or /back | Undo the previous choice and restore the earlier story and item state |
| r or /restart | Start over and clear the current history and items |
| h or /history | Read the current branch's narration, dialogue, and choices |
| i or /inventory | Inspect carried items and remembered decisions |
| ? or /help | Show help and redisplay the current scene and choices |
| q or /quit | Exit |

Chinese command aliases and full-width digits are supported. Responses are predefined choices, not free-text conversation. Items take effect automatically in relevant scenes; there is no separate equip or use command.

Empty input, invalid numbers, and repeated digits such as 11 produce an explanation without advancing the story. Back at the opening explains that there is no earlier choice. At an ending, you can still inspect the log, backtrack, restart, or quit. Ctrl+C and end-of-input exit without a traceback.

## How choices matter

The interaction loop is:

**Choose a reply or action → record its consequences → move to a scene → show visual and textual feedback → offer the currently available choices.**

The four acts are Unread Messages, The City in the Rain, The Bookshop's Last Row, and After the Event. A remote-conversation route skips the scenes inside the bookshop. The act indicator shows the current chapter, not a completion percentage.

Examples of consequences include:

- An **umbrella** lets you cross the rainy street without getting soaked.
- A **power bank** makes a phone call possible while sheltering from the rain.
- An **old notebook** opens additional topics and a possible riverside route.
- Running through the rain can soak that notebook and change its scene.
- Sharing your location or making a vague promise affects later responses.

Earlier choices do not permanently lock you into a “good” or “bad” outcome. Backtracking lets you explore alternatives, with all later decisions and items removed from the current branch.

## Text preview

The actual game uses Chinese narration and choices. This excerpt illustrates the terminal presentation:

~~~text
[*] [ ] [ ] [ ]  第 1 幕 · 未读消息

        .----------------------.
        |  CHAT        [==  ]  |
        |----------------------|
        |  .---------------.   |
        |  |  . . .        |   |
        |  '---------------'   |
        |     .------------.   |
        |     | _          |   |
        |     '------------'   |
        '----------o-----------'

林予 › 你是不是忘了今天的约定？

[1] 回复：对不起，我忘记时间了。我还在家。
[2] 回复：没忘，我马上到！
[3] 回复：才晚了一会儿，不用这么着急吧。

b 返回 · r 重玩 · h 记录 · i 物品 · ? 帮助 · q 退出

你的选择 >
~~~

This is a text preview, **not a terminal screenshot**. An actual runtime screenshot still needs to be added for the assignment submission. A short screen recording is optional; a hosted website is not required for this command-line project.

## Project structure

| File | Purpose |
| --- | --- |
| main.py | Terminal presentation, input handling, history, inventory, and state restoration |
| story.py | Scenes, dialogue, choices, conditions, and endings |
| art.py | Original ASCII scene illustrations |
| pyproject.toml and uv.lock | Project metadata and reproducible environment setup |
| README.md | Default English project documentation |
| README.zh-CN.md | Chinese project documentation |
| [PROCESS.md](PROCESS.md) | Design decisions, reported feedback, iterations, AI use, and validation records, in Chinese |
| [CREDITS.md](CREDITS.md) | Authorship and tool acknowledgements, in Chinese |

### A code path to explain

In main.py, Session.available_choices() filters the current scene's options using state derived from the player's history. Session.choose() maps the displayed number to the actual story choice, saves that choice, and moves to its target node. Terminal.show_node() then displays the corresponding illustration, narration, dialogue, and new options.

Session.flags rebuilds inventory and remembered decisions from history. Session.back() removes the last history entry, so the next state calculation restores the earlier state without retaining items acquired later.

## Development and validation

The initial version was a short conversation. Reported testing feedback described it as too short and insufficiently engaging, and requested symbol-based visuals. The revised version adds a four-act journey, ASCII scenes, item-dependent choices, and later references to earlier decisions. The report does not yet identify whether the tester was someone other than the author; that detail and a human retest of the revision remain to be documented.

The recorded automated checks cover:

- 6,590 reachable scene-and-state combinations, all 33 story scenes, all six ending nodes, and all 78 authored choices.
- State restoration after backtracking, including replacing an umbrella choice with a power bank without keeping both.
- Actual command-line runs reaching each ending variant.
- Inventory, history, help, restart, invalid and full-width input, EOF, and Ctrl+C.
- All 14 illustrations at terminal widths of 28, 60, and 100 columns.

These checks were run during development; they are not a bundled test suite and do not replace a human usability trial. See [PROCESS.md](PROCESS.md) for the record and remaining trial fields.

## Limitations

- The game and dialogue are currently Chinese-only; this README is English documentation.
- Dialogue is authored in advance. There is no runtime AI or natural-language understanding.
- The story depicts fictional people; their reactions are not predictions or rules for real relationships.
- There is no persistent save. Exiting loses the current playthrough.
- Separate valid inputs are processed separately: typing 1 and Enter twice makes two choices. There is no input debounce timer.
- A real terminal screenshot, fuller trial details, and a human retest of the expanded version are still pending.

## Credits and assignment submission

The concept, code, dialogue, ASCII illustrations, and documentation were developed with **OpenAI Codex assistance** under the author's direction. The game itself does not call AI services. No external images, audio, datasets, or copied course-example code are included. Details are recorded in [CREDITS.md](CREDITS.md) and [PROCESS.md](PROCESS.md).

Before submitting the public repository URL on Canvas, add the runtime screenshot, complete the required trial record with at least one other person, review the AI-use statement, and record subsequent changes in genuine Git commits. Git history begins with the publication of this revised project; earlier development is described in PROCESS.md rather than reconstructed as past commits.
