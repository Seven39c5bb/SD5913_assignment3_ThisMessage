from dataclasses import dataclass


@dataclass(frozen=True)
class Choice:
    text: str
    target: str
    gains: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    forbids: tuple[str, ...] = ()

    def available(self, flags: set[str]) -> bool:
        return set(self.requires) <= flags and not set(self.forbids) & flags


@dataclass(frozen=True)
class Detail:
    text: str
    requires: tuple[str, ...] = ()
    forbids: tuple[str, ...] = ()

    def available(self, flags: set[str]) -> bool:
        return set(self.requires) <= flags and not set(self.forbids) & flags


@dataclass(frozen=True)
class Scene:
    title: str
    chapter: int
    art: str
    narration: tuple[str, ...]
    messages: tuple[str, ...]
    choices: tuple[Choice, ...]
    details: tuple[Detail, ...] = ()


@dataclass(frozen=True)
class Ending:
    title: str
    art: str
    narration: tuple[str, ...]
    messages: tuple[str, ...]
    reflection: str


CHAPTERS = ("未读消息", "雨中的城市", "书店的最后一排", "散场之后")
ITEMS = {"notebook": "旧手册", "umbrella": "折叠伞", "charger": "充电宝"}
MEMORIES = {
    "honest": "说清了自己还在家",
    "bluff": "最初说了含糊的「马上」",
    "listened": "听完了对方的解释",
    "flyer": "看过书店活动单",
    "checked_in": "路上主动更新了位置",
    "wet": "冒雨赶路，手册也可能淋湿",
    "heard": "听见了分享会的最后一段",
    "moving": "得知林予周五搬走",
    "voice": "打过一次电话",
}

SCENES = {
    "start": Scene("19:42 / 手机亮了", 1, "phone",
        ("窗外刚起风。电脑上还有没做完的东西，你伸手去拿水，碰亮了手机。",
         "你们约好 19:30 在旧书店见面。分享会 20:00 开始；从家里过去至少四十分钟。"),
        ("你是不是忘了今天的约定？",), (
            Choice("回复：对不起，我忘记时间了。我还在家。", "honest", ("honest",)),
            Choice("回复：没忘，我马上到！", "promise", ("bluff",)),
            Choice("回复：才晚了一会儿，不用这么着急吧。", "defensive"),
        )),
    "honest": Scene("19:43 / 没有省略号了", 1, "phone",
        ("『对方正在输入』闪了一下，又消失了。几秒后，两条消息一起到达。",),
        ("好。谢谢你直接告诉我。", "我不是非要你赶上开场，只是不想一直站在门口猜。"), (
            Choice("回复：你先进去。今晚为什么特别想来这场活动？", "context", ("listened",)),
            Choice("回复：我先收拾出门，到路上再给你准确消息。", "context"),
        )),
    "promise": Scene("19:43 / 一句「马上」", 1, "phone",
        ("你还穿着拖鞋。手机上的导航显示：最快四十一分钟。",),
        ("到哪个站了？我帮你留一下门口的位置。",), (
            Choice("回复：其实还在家。刚才怕你生气，说得太快了。", "context", ("honest",)),
            Choice("回复：别等在门口了，我出发后告诉你。", "context"),
        )),
    "defensive": Scene("19:43 / 回复框里的光标", 1, "phone",
        ("你打了半句解释，删掉；又打了半句。对方先发了过来。",),
        ("我不是在催你。", "我只是有件事，想今天当面跟你说。"), (
            Choice("回复：我刚才语气不好。你说，我在听。", "context", ("listened",)),
            Choice("回复：什么事？我收拾一下就出门。", "context"),
        )),
    "context": Scene("19:45 / 『等见面再说』", 1, "room",
        ("雨点开始敲窗。桌上压着一张活动单，下面露出一本边角卷起的小手册。",),
        ("这场活动叫『给城市的一封信』。", "那件事等见面再说吧。你先看好路线，不用硬赶开场。"), (
            Choice("看看桌上的旧手册。", "notebook"),
            Choice("展开那张活动单。", "flyer"),
            Choice("先不翻东西，去门边收拾。", "pack"),
        )),
    "notebook": Scene("19:47 / 城市没有走完", 1, "book",
        ("手册是你们去年画的『周末散步地图』。第一页的面包店已经打了勾。",
         "最后一页只有一条虚线：书店 → 河边。旁边是林予的字：『这段下次一起走。』"), (), (
            Choice("把手册放进口袋，今晚带给林予。", "pack", ("notebook",)),
            Choice("合上手册。先把今晚的迟到处理好。", "pack"),
        )),
    "flyer": Scene("19:47 / 活动单背面", 1, "book",
        ("活动单背面写着：『离开一座城市前，你想带走什么？』",
         "你这才注意到，林予上周发来的纸箱照片，并不是在整理房间。"), (), (
            Choice("拍下这句话，记得见面时问问。", "pack", ("flyer",)),
            Choice("把它重新压平，先出门。", "pack"),
        )),
    "pack": Scene("19:49 / 门边的最后一件东西", 1, "bag",
        ("钥匙、手机已经拿好。你只想带一个小包，剩下的位置够装一件东西。",
         "折叠伞和充电宝都在柜子上。手机只剩 12% 电，雨声越来越密。"), (), (
            Choice("带折叠伞。", "route", ("umbrella",)),
            Choice("带充电宝。", "route", ("charger",)),
            Choice("什么也不带，轻装出门。", "route"),
        )),
    "route": Scene("19:51 / 电梯门打开", 2, "city",
        ("楼下便利店的灯映在积水里。三个方向，都能走到那家书店。",
         "导航时间只是估计。你需要决定一路上怎样应对变化。"), (), (
            Choice("去地铁站：大部分路段不用淋雨。", "station"),
            Choice("走河边步道：近一些，但没有遮挡。", "bridge"),
            Choice("等公交：能在书店街口下车。", "bus"),
        )),
    "station": Scene("19:57 / 临时停运", 2, "train",
        ("站台响起广播：前方设备检查，下一班车预计延误十分钟。",
         "玻璃上映出一排低头看手机的人。你的屏幕又亮了。"),
        ("我进场了，结束大概九点。你还顺利吗？",), (
            Choice("回复：地铁延误了。我在站台，八点半前再更新一次。", "platform", ("checked_in",)),
            Choice("先不回复，等车来了再说。", "platform"),
        )),
    "platform": Scene("20:09 / 车窗里的倒影", 2, "train",
        ("列车终于来了。你坐在车门旁，隧道里的灯一格格掠过。",
         "你翻到林予之前发的照片：两只纸箱，一盆用胶带固定的绿植。"), (), (
            Choice("发消息：刚上车。活动结束我在书店外等你。", "rain", ("checked_in",)),
            Choice("收起手机，先想想见面要说什么。", "rain"),
        )),
    "bridge": Scene("20:02 / 桥上的风", 2, "bridge",
        ("你走上河边的小桥。远处书店的招牌很小，雨却比楼下大得多。",
         "手机震了一下。林予已经进场，问你还顺不顺利。"), (), (
            Choice("停在桥头，发一句：我走河边过来，雨大，可能慢一点。", "river", ("checked_in",)),
            Choice("把手机塞回口袋，先过桥。", "river"),
        )),
    "river": Scene("20:15 / 没画完的路线", 2, "bridge",
        ("经过河边的旧售票亭时，你想起去年那次没走完的散步。",
         "那时你们也说过『下次吧』，只是后来一直没找到那个下次。"), (), (
            Choice("停一会儿，记住这条路。", "rain"),
            Choice("拍下路牌，发消息告诉林予快到书店街了。", "rain", ("checked_in",)),
        ), (Detail("口袋里的手册抵着掌心。最后一页的虚线，原来就在脚下。", ("notebook",)),)),
    "bus": Scene("20:00 / 站牌下", 2, "bus",
        ("电子站牌从『3 分钟』跳成了『9 分钟』。旁边的人笑了一声：它刚才也是这么说的。",
         "林予发来一句：『我进场了，结束大概九点。』"), (), (
            Choice("回复：公交还没来。我会更新位置，你安心看。", "busride", ("checked_in",)),
            Choice("再等等，暂时不发消息。", "busride"),
        )),
    "busride": Scene("20:13 / 倒着走的霓虹", 2, "bus",
        ("车来了。你坐到靠窗的位置，雨水把招牌上的字拉成彩色的长线。",
         "手机又掉了一格电。书店还有四站。"), (), (
            Choice("给林予发站牌位置，说明已经上车。", "rain", ("checked_in",)),
            Choice("开启省电模式，等到了再联系。", "rain"),
        )),
    "rain": Scene("20:28 / 书店街口", 2, "rain",
        ("下车或走到街口时，你离书店只剩一段露天小街。雨幕把招牌遮了一半。",
         "旁边的屋檐可以避雨。手机提示低电量，你看了一眼包。"), (), (
            Choice("撑开折叠伞，沿着招牌走过去。", "entrance", requires=("umbrella",)),
            Choice("护着手机，直接跑过雨里的小街。", "entrance", ("wet",), forbids=("umbrella",)),
            Choice("先到屋檐下避雨，再决定怎么联系。", "shelter"),
        ), (Detail("你接上充电宝，屏幕重新亮了起来。", ("charger",)),)),
    "shelter": Scene("20:32 / 屋檐下的两分钟", 2, "rain",
        ("屋檐滴水连成一条线。你终于停下来，不再一边赶路一边想怎么解释。",), (), (
            Choice("插着充电宝，给林予打个简短电话。", "call", ("voice", "checked_in"), ("charger",)),
            Choice("发短信：我在街口避雨，等雨小些就到门口。", "entrance", ("checked_in",)),
            Choice("发短信：今晚可能不适合硬赶。等结束后，我们远程聊聊？", "remote", ("checked_in",)),
        ), (Detail("没带充电宝，电量已经见底。你把仅剩的电留给文字消息。", forbids=("charger",)),)),
    "call": Scene("20:34 / 电话另一端", 2, "phone",
        ("林予走到活动室外接电话。背景里有人试麦，你听见了一声很轻的笑。",),
        ("你怎么像在瀑布里？", "别急，我周五才搬。今晚还有时间。……本来想当面说的。"), (
            Choice("回复：搬走？我想听你说。我到书店门口等。", "entrance", ("moving",)),
            Choice("回复：那今晚先别赶了。活动结束我们再通话，好吗？", "remote", ("moving",)),
        )),
    "entrance": Scene("20:42 / 迟到的人", 3, "bookshop",
        ("书店门口的地垫吸满了水。里面坐着十几个人，只剩最后一排有空位。",
         "店员指了指后排，又指向旁边的书架：『想坐就轻一点进去。』"), (), (
            Choice("轻轻坐进最后一排，听完剩下的部分。", "hall", ("heard",)),
            Choice("先在外面的书架旁等，翻翻活动相关的书。", "shelves"),
        ), (
            Detail("手机上有一条回复：『看到你的更新了，知道你会来。最后一排见。』", ("checked_in",)),
            Detail("手机上堆了两条未读消息：『到哪里了？』『我先听活动了。』", forbids=("checked_in",)),
            Detail("袖口还在滴水。你把口袋里的纸张摊开，边角已经发皱。", ("wet",)),
        )),
    "hall": Scene("20:50 / 留下来的一句话", 3, "hall",
        ("台上的人正在读信：『我们总把下次说得很轻，好像它一定会来。』",
         "林予回头看见你，朝空座位点了点头。没有责备，也没有立刻说话。"), (), (
            Choice("安静听完，把这句话记下来。", "shelves"),
            Choice("把手机扣在膝上，向林予点头示意。", "shelves"),
        )),
    "shelves": Scene("20:58 / 一本打包好的书", 3, "book",
        ("分享会快结束了。柜台上放着一本包好的书，便签上写着你的名字。",
         "林予从里面出来，看见你盯着它，说：『原本想今天给你的。』"),
        ("我周五搬去另一座城市。东西都装箱了。", "这本书借了你一年，总得当面还。"), (
            Choice("回复：难怪你想约今天。刚才只顾着解释迟到了。", "exit", ("moving", "listened")),
            Choice("回复：什么时候决定的？我们找个地方慢慢说。", "exit", ("moving",)),
        ), (Detail("活动单上的『离开一座城市』，这时终于有了具体的意思。", ("flyer",)),)),
    "exit": Scene("21:03 / 门口的空地", 3, "bookshop",
        ("人群散去。林予把那本书递给你，封面还留着你以前折过的痕迹。",
         "你们并排站在门口。雨小了一点，街角的咖啡店还开着。"), (), (
            Choice("拿出那本没走完的散步手册。", "map", requires=("notebook",), forbids=("wet",)),
            Choice("拿出被雨淋皱的手册，摊开最后一页。", "wetmap", requires=("notebook", "wet")),
            Choice("提议去街角喝点热的，把话聊完。", "cafe"),
            Choice("问问林予：你想现在聊，还是明天再说？", "boundary"),
        )),
    "map": Scene("21:05 / 那条虚线", 4, "map",
        ("你把手册翻到最后一页。林予低头看了很久，然后用指尖沿虚线划了一遍。",),
        ("你还留着。", "河边那一段，我一直以为我们会找一天走完。"), (
            Choice("回复：雨小了。今晚把这一段走完？", "walk", requires=("umbrella",)),
            Choice("回复：没有伞，我们先去咖啡店把路线画完。", "cafe", forbids=("umbrella",)),
            Choice("回复：别再写『下次』了。周四晚上七点，在桥头见？", "appointment"),
        )),
    "wetmap": Scene("21:05 / 墨水晕开的地方", 4, "map",
        ("手册的纸粘在一起，最后一页的河流和虚线晕成了一团蓝色。",
         "林予没有笑你，只说：『看上去我们已经游过这条河了。』你们终于一起笑了。"), (), (
            Choice("提议去咖啡店，借支笔重新画一遍。", "cafe"),
            Choice("回复：地图坏了，约定还可以重写。周四七点桥头见？", "appointment"),
        )),
    "cafe": Scene("21:12 / 两杯热饮", 4, "cafe",
        ("咖啡店只剩窗边一张小桌。杯子升起的热气把玻璃熏白了一小块。",
         "林予说新住处窗台很窄，那盆绿植可能只能摆到地上。你忽然不知道先接哪句话。"), (), (
            Choice("先问：你对搬走这件事，是期待多一点，还是舍不得多一点？", "confession", ("listened",)),
            Choice("先说：今天的事，我想好好解释，也想听听你。", "confession"),
            Choice("打个岔：以后你要靠远程指导我养那盆绿植了。", "confession"),
        ), (
            Detail("旧手册摊在两只杯子中间，林予顺手拿起了笔。", ("notebook",)),
            Detail("你提起台上那句『下次』。林予说，那也是自己记住的一句。", ("heard",)),
        )),
    "confession": Scene("21:25 / 不只是今天", 4, "cafe",
        ("对话慢下来。你们说起没去成的展览、借来的书，还有已经关掉的面包店。",),
        ("其实都有。搬走有点兴奋，也怕以后每次联系都得找一个很正式的理由。",
         "今天等你的时候，我怕的不是十二分钟，是我们又把见面推给下一次。"), (
            Choice("回复：我不能保证每次都做得好，但可以从一个具体约定开始。", "appointment"),
            Choice("回复：今晚先不急着安排以后。我想把你现在的感受听完。", "quiet"),
            Choice("回复：可我已经赶过来了，为什么还要翻以前的事？", "fracture"),
        ), (
            Detail("林予又说：『刚才那个马上让我很失落，不过后来你把真实情况说清楚了。』", ("bluff", "honest")),
            Detail("林予又说：『你最初说马上到的时候，我真的又站在门口等了一阵。』", ("bluff",), ("honest",)),
            Detail("你路上发过的位置，让这段谈话少了一次对迟到的反复解释。", ("checked_in",)),
        )),
    "appointment": Scene("21:31 / 把『下次』写下来", 4, "map",
        ("林予打开日历。你们认真确认了一次时间，而不是随口说『有空再约』。",),
        ("周四晚上七点，桥头。赶不上就提前说，不用再编一个『马上』。",), (
            Choice("确认约定，并记进手机日历。", "promise_kept"),
            Choice("先确认自己的安排：如果不确定，我明天中午前答复你。", "quiet"),
        )),
    "walk": Scene("21:18 / 一把伞的宽度", 4, "bridge",
        ("你撑开伞，林予拿着手册。你们从书店慢慢走到河边，不再看导航上的分钟数。",
         "桥头正好有一块干燥的石栏，可以把最后一页摊平。"),
        ("原来这段路比我们想的短。",), (
            Choice("让林予画最后一笔，你写上今晚的日期。", "last_page"),
            Choice("先别急着画完。问问林予，搬走以后想去哪里散步。", "quiet"),
        )),
    "boundary": Scene("21:06 / 给今天留一点空白", 4, "bench",
        ("林予抱着还没送出的活动单，看了一眼街角的灯，又看了一眼手机。",),
        ("我想回去再装一点东西。今天先到这里，可以吗？",), (
            Choice("回复：可以。明天中午我联系你，你再决定想不想聊。", "remote_plan"),
            Choice("回复：我有点失落，但我听到了。让我陪你等车吧。", "quiet"),
            Choice("回复：我跑来这一趟，你却现在要走？", "fracture"),
        )),
    "remote": Scene("21:04 / 隔着一场雨", 4, "phone",
        ("你提前说明了今晚的变化，先回到可以充电的地方。九点刚过，屏幕亮起。",
         "活动已经结束。林予发来一张照片：一本包好的旧书，便签上写着你的名字。"),
        ("周五我要搬走。这本书本来想今晚还给你。",), (
            Choice("回复：我想听听你的想法。你愿意现在讲讲吗？", "remote_talk", ("moving", "listened")),
            Choice("回复：我很想听，但如果你累了，我们可以约好明天聊。", "remote_plan", ("moving",)),
        )),
    "remote_talk": Scene("21:15 / 信号另一端", 4, "phone",
        ("充上电以后，你们断断续续聊了十分钟。窗外的雨声没有消失，只是不再那么急。",),
        ("我怕搬走以后，就连见一面都得提前很久预约。",), (
            Choice("回复：那明晚八点先通个电话。你给我看看打包到哪了。", "remote_plan"),
            Choice("回复：今晚不急着挂。我想听听你准备怎么布置新房间。", "quiet_remote"),
        )),
    "remote_plan": Scene("21:20 / 一个可执行的安排", 4, "phone",
        ("你们没有把这一晚解释成完美的一晚，也没有逼着彼此立刻消化所有情绪。",),
        ("明晚八点打电话吧。书先在我这里，见面的时候再还。",), (
            Choice("回复：好，明晚八点。我会提前确认。", "space"),
            Choice("回复：八点还不确定。我明天中午前给你答复，不让你空等。", "space"),
        )),
    "fracture": Scene("21:28 / 一句话之后", 4, "bench",
        ("林予把视线移开。你忽然听见街上的车声，比刚才清楚得多。",),
        ("我知道你来了。但我也可以累，也可以还没准备好继续聊。",), (
            Choice("停下来：对不起，我又只顾着自己的感受了。今晚先停在这里。", "space"),
            Choice("回复：那就这样吧。", "apart"),
        )),
}

ENDINGS = {
    "last_page": Ending("最后一页，有了日期", "map",
        ("虚线终于连到河边。林予在日期旁画了一把小伞，你补了两双歪歪扭扭的鞋。",
         "搬走的日子没有改变，迟到也没有被抹去。但这次，地图上不再写着『下次』。"),
        ("这本手册你留着吧。下一个城市，我们从新的一页开始。",),
        "你带上了旧手册和伞，也在见面后提出一起走完那段路。物品与行动共同留下了这个结尾。"),
    "promise_kept": Ending("下次，不再只是两个字", "bookshop",
        ("日历上多了一个具体的时间。你收好那本书，林予叮嘱别再把书签夹丢了。",),
        ("周四见。要有变化，提前说就好。",),
        "这一晚结束在一个可确认的安排上。它不是已经兑现的承诺，下一次行动仍然重要。"),
    "quiet": Ending("把话听完的夜晚", "city",
        ("你们没有急着把关系修好，也没有列出以后的所有计划。",
         "一段话接着另一段话，有时也只是一起安静地待着。时间终于不只用来赶路。"),
        ("谢谢你没急着替我想好答案。",),
        "你选择让这次见面继续，而不是马上寻找一个圆满结论。"),
    "quiet_remote": Ending("把话听完的夜晚", "phone",
        ("你靠着椅背听林予描述新房间。电话里传来胶带拉开的声音，窗外的雨慢慢停了。",),
        ("我给你看看窗台吧，小得有点好笑。",),
        "今晚没有见成面，但你留出了真实的时间。这个结局发生在电话两端。"),
    "space": Ending("给彼此留一点空间", "bench",
        ("这一天没有照原计划结束。你们把谈不完的部分留了下来，没有再用一句『马上』填上。",),
        ("好，我们之后再联系。",),
        "暂停也是一种决定。重要的是，对方不必继续猜测你现在准备做什么。"),
    "apart": Ending("今晚，停在这里", "rain",
        ("你们分别走进两边的街道。聊天窗口停在最后一句，输入框里没有再出现光标。",), (),
        "今晚的交流中断了。可以返回那个让你在意的选择，试试另一条路。"),
}


def validate_story() -> None:
    overlap = set(SCENES) & set(ENDINGS)
    if overlap:
        raise ValueError(f"重复节点：{sorted(overlap)}")
    visited = set()
    active = set()

    def visit(node_id: str) -> None:
        if node_id in active:
            raise ValueError(f"故事存在循环：{node_id}")
        if node_id in visited:
            return
        if node_id in ENDINGS:
            visited.add(node_id)
            return
        if node_id not in SCENES:
            raise ValueError(f"找不到节点：{node_id}")
        scene = SCENES[node_id]
        if not scene.choices or not 1 <= scene.chapter <= len(CHAPTERS):
            raise ValueError(f"节点设置无效：{node_id}")
        active.add(node_id)
        for choice in scene.choices:
            if set(choice.requires) & set(choice.forbids):
                raise ValueError(f"选项条件冲突：{node_id}")
            visit(choice.target)
        active.remove(node_id)
        visited.add(node_id)

    visit("start")
    missing = (set(SCENES) | set(ENDINGS)) - visited
    if missing:
        raise ValueError(f"无法到达：{sorted(missing)}")
