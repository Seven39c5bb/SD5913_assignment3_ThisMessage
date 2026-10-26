import argparse
import os
import shutil
import sys
import unicodedata
from dataclasses import dataclass, field

from art import ART
from story import CHAPTERS, ENDINGS, ITEMS, MEMORIES, SCENES, validate_story


@dataclass
class Session:
    node_id: str = "start"
    history: list[tuple[str, int]] = field(default_factory=list)

    @property
    def flags(self) -> set[str]:
        result = set()
        for node_id, choice_index in self.history:
            result.update(SCENES[node_id].choices[choice_index].gains)
        return result

    def available_choices(self) -> list:
        if self.node_id in ENDINGS:
            return []
        flags = self.flags
        return [
            (index, choice)
            for index, choice in enumerate(SCENES[self.node_id].choices)
            if choice.available(flags)
        ]

    def choose(self, number: int) -> str:
        if self.node_id in ENDINGS:
            return "这里已经是结局。输入 b 返回，r 重玩，或 q 退出。"
        choices = self.available_choices()
        if not 1 <= number <= len(choices):
            return f"没有推进剧情。请输入 1–{len(choices)} 中的一个数字。"
        choice_index, choice = choices[number - 1]
        self.history.append((self.node_id, choice_index))
        self.node_id = choice.target
        return ""

    def back(self) -> bool:
        if not self.history:
            return False
        self.node_id, _ = self.history.pop()
        return True

    def restart(self) -> None:
        self.node_id = "start"
        self.history.clear()


def display_width(text: str) -> int:
    return sum(
        0 if unicodedata.combining(character) else
        2 if unicodedata.east_asian_width(character) in ("W", "F") else 1
        for character in text
    )


def wrap_text(text: str, width: int) -> list[str]:
    lines = []
    current = ""
    current_width = 0
    for character in text:
        character_width = display_width(character)
        if character == "\n":
            lines.append(current)
            current, current_width = "", 0
        else:
            if current and current_width + character_width > width:
                lines.append(current)
                current, current_width = "", 0
            current += character
            current_width += character_width
    if current or not lines:
        lines.append(current)
    return lines


class Terminal:
    def __init__(self, plain: bool = False, no_art: bool = False) -> None:
        terminal_supports_color = os.name != "nt" or any(
            os.environ.get(variable) for variable in ("WT_SESSION", "ANSICON", "TERM_PROGRAM")
        )
        self.color = (
            not plain and sys.stdout.isatty() and terminal_supports_color
            and "NO_COLOR" not in os.environ and os.environ.get("TERM") != "dumb"
        )
        self.no_art = no_art

    @property
    def width(self) -> int:
        return max(12, min(84, shutil.get_terminal_size((80, 24)).columns - 4))

    def say(self, text: str = "", style: str = "0") -> None:
        for line in wrap_text(text, self.width):
            rendered = f"\033[{style}m{line}\033[0m" if self.color else line
            print(f"  {rendered}")

    def rule(self) -> None:
        self.say("─" * self.width, "90")

    def picture(self, art_id: str) -> None:
        if self.no_art:
            return
        label, drawing = ART[art_id]
        lines = drawing.strip("\n").splitlines()
        if max(map(display_width, lines)) <= self.width:
            for line in lines:
                self.say(line, "36")
        self.say(f"[ {label} ]", "90")
        self.say()

    def introduction(self) -> None:
        self.rule()
        self.say("这条消息怎么回？", "1;36")
        self.say("THIS MESSAGE  /  雨夜，和那些没说完的话", "90")
        self.say("四幕互动故事 · 五种结局主题 · 选择回复，也选择行动")
        self.rule()
        self.say("输入数字并按 Enter 选择。物品和之前的决定会改变后续选项。")
        self.say("b 返回  ·  r 重玩  ·  h 记录  ·  i 随身物品  ·  ? 帮助  ·  q 退出", "90")
        self.say("符号画面建议用等宽字体。没有实时倒计时，慢慢读即可。", "90")
        self.say("虚构离线故事；不会发送真实消息，退出后不保存进度。", "90")

    def scene_text(self, node_id: str, flags: set[str]) -> None:
        node = ENDINGS.get(node_id) or SCENES[node_id]
        for paragraph in node.narration:
            self.say(paragraph)
        if node_id in SCENES:
            for detail in node.details:
                if detail.available(flags):
                    self.say(detail.text, "90")
        if node.messages:
            self.say()
            for message in node.messages:
                self.say(f"林予 › {message}", "36")

    def show_node(self, session: Session) -> None:
        self.say()
        self.rule()
        flags = session.flags
        if session.node_id in ENDINGS:
            ending = ENDINGS[session.node_id]
            self.say(f"终幕 / {ending.title}", "1;33")
            self.picture(ending.art)
            self.scene_text(session.node_id, flags)
            self.say()
            self.say(ending.reflection, "90")
            self.say(f"这一轮做了 {len(session.history)} 次选择。输入 h 可回看完整旅程。", "90")
            self.say("b 改选上一项  ·  r 从头开始  ·  i 回看物品  ·  q 退出", "90")
            return
        scene = SCENES[session.node_id]
        progress = " ".join("[*]" if chapter <= scene.chapter else "[ ]" for chapter in range(1, 5))
        self.say(f"{progress}  第 {scene.chapter} 幕 · {CHAPTERS[scene.chapter - 1]}", "1")
        self.say(f"{scene.title}  /  第 {len(session.history) + 1} 次选择", "90")
        self.picture(scene.art)
        self.scene_text(session.node_id, flags)
        self.say()
        for number, (_, choice) in enumerate(session.available_choices(), start=1):
            self.say(f"[{number}] {choice.text}", "33")
        self.say()
        inventory = "、".join(["手机", "钥匙"] + [label for flag, label in ITEMS.items() if flag in flags])
        self.say(f"随身：{inventory}", "90")
        self.say("b 返回 · r 重玩 · h 记录 · i 物品 · ? 帮助 · q 退出", "90")

    def show_history(self, session: Session) -> None:
        self.rule()
        self.say("当前分支的旅程记录（返回过的分支不保留）", "1")
        flags = set()
        for node_id, choice_index in session.history:
            scene = SCENES[node_id]
            self.say()
            self.say(scene.title, "1")
            self.scene_text(node_id, flags)
            choice = scene.choices[choice_index]
            self.say(f"你选择 › {choice.text}", "35")
            flags.update(choice.gains)
        self.say()
        self.scene_text(session.node_id, flags)
        self.say("记录结束。输入编号继续，或输入 ? 重新显示当前场景。", "90")

    def show_inventory(self, session: Session) -> None:
        flags = session.flags
        self.rule()
        self.say("随身物品与已经发生的事", "1")
        self.say("手机、钥匙（始终携带）")
        for flag, label in ITEMS.items():
            if flag in flags:
                self.say(f"+ {label}", "33")
        for flag, label in MEMORIES.items():
            if flag in flags:
                self.say(f"· {label}", "90")
        self.say("物品在相关场景自动发挥作用；没有额外的装备命令。", "90")
        self.say("输入编号继续，或输入 ? 重新显示当前场景。", "90")


def run_game(terminal: Terminal, demo: bool = False) -> None:
    session = Session()
    terminal.introduction()
    if demo:
        terminal.say("演示模式：每步自动选择第一个可用选项，直到结局。", "33")
    terminal.show_node(session)
    while True:
        try:
            if demo:
                command = "q" if session.node_id in ENDINGS else "1"
                terminal.say(f"> {command}", "90")
            else:
                command = input("\n  你的选择 > ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            terminal.say()
            terminal.say("故事已关闭。没有保存进度，下次可以从头再试。")
            return
        if command in ("q", "/quit", "退出"):
            terminal.say("故事已关闭。愿下一条消息，能把想说的话带到。")
            return
        if command in ("b", "/back", "返回"):
            if session.back():
                terminal.say("已返回上一项。后续剧情、物品与决定一并撤回。", "90")
                terminal.show_node(session)
            else:
                terminal.say("已经在开场，没有更早的选择可以返回。", "33")
        elif command in ("r", "/restart", "重玩"):
            session.restart()
            terminal.say("新的一轮开始了。记录、物品与决定已重置。", "90")
            terminal.show_node(session)
        elif command in ("h", "/history", "记录"):
            terminal.show_history(session)
        elif command in ("i", "/inventory", "物品"):
            terminal.show_inventory(session)
        elif command in ("?", "/help", "帮助"):
            terminal.say("输入选项编号并按 Enter；不能自由输入对白。b 返回，r 重玩，h 记录，i 物品，q 退出。")
            terminal.say("不同物品和决定会改变选项；返回会恢复当时的状态。退出不保存。")
            terminal.show_node(session)
        elif len(command) == 1 and unicodedata.normalize("NFKC", command) in "123456789":
            number = int(unicodedata.normalize("NFKC", command))
            error = session.choose(number)
            if error:
                terminal.say(error, "33")
            else:
                previous_node, choice_index = session.history[-1]
                choice = SCENES[previous_node].choices[choice_index]
                terminal.say(f"你选择 › {choice.text}", "35")
                if choice.gains:
                    for flag in choice.gains:
                        if flag in ITEMS:
                            terminal.say(f"已带上：{ITEMS[flag]}", "90")
                terminal.show_node(session)
        else:
            message = "还没有输入内容。" if not command else "没有推进剧情；这不是有效选项或命令。"
            terminal.say(f"{message} 输入当前编号，或输入 ? 查看帮助。", "33")


def main() -> None:
    parser = argparse.ArgumentParser(description="这条消息怎么回？——四幕中文命令行互动故事")
    parser.add_argument("--plain", action="store_true", help="关闭彩色文字，保留符号画面")
    parser.add_argument("--no-art", action="store_true", help="隐藏符号画面，适合紧凑显示或屏幕阅读器")
    parser.add_argument("--demo", action="store_true", help="自动演示一条完整路线")
    arguments = parser.parse_args()
    for stream in (sys.stdin, sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    validate_story()
    for node in (*SCENES.values(), *ENDINGS.values()):
        if node.art not in ART:
            raise ValueError(f"缺少场景画面：{node.art}")
    run_game(Terminal(plain=arguments.plain, no_art=arguments.no_art), demo=arguments.demo)


if __name__ == "__main__":
    main()
