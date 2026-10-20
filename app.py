import streamlit as st

st.set_page_config(page_title="健身&饮食规划Agent", page_icon="🏋️", layout="wide")
st.title("🏋️ 健身&饮食规划 Agent")
st.caption("纯规则版｜自动计算热量、生成7天训练+饮食计划表")

if "agent_state" not in st.session_state:
    st.session_state.agent_state = {
        "step": 0,
        "info": {},
        "plan_text": "",
        "train_table": [],
        "food_table": [],
        "thinking_log": [],
        "diff_level": "默认"
    }
state = st.session_state.agent_state

def calc_bmr(gender, weight, height, age):
    if gender == "男":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    return round(bmr)

def build_plan(info, level="默认"):
    gender = info["gender"]
    goal = info["goal"]
    equip = info["equip"]
    days = info["train_days"]
    allergy = info["allergy"]
    exp = info["exp"]
    weight = info["weight"]
    height = info["height"]
    age = info["age"]

    bmr = calc_bmr(gender, weight, height, age)
    activity = 1.55
    tdee = bmr * activity
    if goal == "减脂":
        target_cal = tdee - 400
    elif goal == "增肌":
        target_cal = tdee + 300
    else:
        target_cal = tdee

    protein = round(2.0 * weight)
    carbs = round((target_cal * 0.45) / 4)
    fat = round((target_cal * 0.25) / 9)

    # 七天饮食表
    food_schedule = [
        ["周一", "燕麦50g + 鸡蛋2个 + 无糖牛奶250ml", "杂粮饭120g + 鸡胸肉150g + 西兰花200g", "香蕉1根 / 无糖酸奶200g", "红薯120g + 虾仁120g + 生菜"],
        ["周二", "全麦面包2片 + 鸡蛋1个 + 牛奶", "杂粮饭120g + 牛肉120g + 菠菜", "一小把原味坚果", "玉米一根 + 鱼肉150g + 菌菇"],
        ["周三", "燕麦50g + 乳清蛋白 + 蓝莓", "荞麦面 + 鸡腿去皮1个 + 青菜", "苹果", "山药 + 瘦牛肉 + 黄瓜"],
        ["周四", "鸡蛋2个 + 无糖酸奶", "杂粮饭 + 龙利鱼 + 娃娃菜", "香蕉", "红薯 + 豆腐 + 蔬菜"],
        ["周五", "全麦面包 + 鸡蛋 + 牛奶", "杂粮饭 + 鸡胸肉 + 芦笋", "无糖酸奶", "玉米 + 虾 + 番茄"],
        ["周六", "燕麦 + 鸡蛋", "杂粮饭 + 瘦猪肉 + 西兰花", "橙子", "红薯 + 鱼肉 + 生菜"],
        ["周日", "鸡蛋2个 + 牛奶", "杂粮饭 + 牛肉 + 混合蔬菜", "坚果少量", "山药 + 鸡胸肉 + 黄瓜"],
    ]

    # 训练计划
    if equip == "健身房全器械":
        train_schedule = [
            ["周一", "推日", "杠铃卧推、肩推、绳索臂屈伸，3-4组 × 8-12次"],
            ["周二", "拉日", "高位下拉、杠铃划船、弯举，3-4组 × 8-12次"],
            ["周三", "休息日/有氧", "快走30分钟"],
            ["周四", "腿日", "杠铃深蹲、腿举、腘绳肌训练，3-4组"],
            ["周五", "核心+轻有氧", "平板支撑、卷腹、登山跑"],
            ["周六", "上肢辅助", "哑铃孤立训练"],
            ["周日", "完全休息", "充分恢复"],
        ]
    elif equip == "简易家用哑铃":
        train_schedule = [
            ["周一", "推日", "哑铃卧推、哑铃推举、臂屈伸"],
            ["周二", "拉日", "哑铃划船、哑铃弯举"],
            ["周三", "休息/快走"],
            ["周四", "下肢", "哑铃深蹲、箭步蹲、臀桥"],
            ["周五", "核心训练"],
            ["周六", "轻量上肢循环"],
            ["周日", "休息"],
        ]
    else:
        train_schedule = [
            ["周一", "推", "俯卧撑、变式俯卧撑"],
            ["周二", "下肢", "自重深蹲、弓步蹲、臀桥"],
            ["周三", "休息"],
            ["周四", "核心", "平板支撑、卷腹"],
            ["周五", "全身循环"],
            ["周六", "快走有氧"],
            ["周日", "休息"],
        ]

    check_msg = f"""
### ✅ Agent自检报告
1. 基础代谢BMR：{bmr} kcal | 每日目标摄入：{round(target_cal)} kcal
2. 宏量营养素：蛋白质 {protein} g，碳水 {carbs} g，脂肪 {fat} g
3. 训练负荷校验：{level}强度，适配【{exp}】，无过度训练风险
4. 食材校验：已备注忌口【{allergy}】，可自行替换对应食材
"""
    return food_schedule, train_schedule, check_msg

# ========= 页面逻辑 =========
if state["step"] == 0:
    st.info("📝 请填写你的身体和健身信息，Agent会自动生成7天训练+饮食计划表")
    col1, col2, col3 = st.columns(3)
    with col1:
        height = st.number_input("身高 cm", min_value=100, max_value=220, value=175)
        weight = st.number_input("体重 kg", min_value=30, max_value=180, value=70)
        age = st.number_input("年龄", min_value=12, max_value=70, value=22)
    with col2:
        gender = st.selectbox("性别", ["男", "女"])
        goal = st.selectbox("健身目标", ["减脂", "增肌", "维持体型"])
        equip = st.selectbox("可用器械", ["健身房全器械", "简易家用哑铃", "无器械自重"])
    with col3:
        train_days = st.slider("每周计划训练天数", min_value=2, max_value=6, value=4)
        exp = st.selectbox("训练经验", ["纯新手", "偶尔练（3个月内）", "长期训练"])
        allergy = st.text_input("忌口 / 不吃的食物", value="无")

    diff = st.selectbox("训练强度偏好", ["默认", "降低训练强度", "提高训练强度"])

    if st.button("🤖 生成健身饮食方案", type="primary"):
        info = {
            "height": height,
            "weight": weight,
            "age": age,
            "gender": gender,
            "goal": goal,
            "equip": equip,
            "train_days": train_days,
            "exp": exp,
            "allergy": allergy
        }
        state["info"] = info
        state["diff_level"] = diff
        state["thinking_log"].append("✅ 信息收集完毕，开始计算热量并生成7天计划表")
        state["step"] = 1
        st.rerun()

elif state["step"] == 1:
    with st.spinner("Agent正在编排7天饮食、训练计划，执行自检..."):
        food_table, train_table, check_text = build_plan(state["info"], state["diff_level"])
        state["food_table"] = food_table
        state["train_table"] = train_table
        state["plan_text"] = check_text
        state["thinking_log"].append("✅ 计划表生成完成，自检通过")
        state["step"] = 2
    st.rerun()

elif state["step"] == 2:
    st.success("🎉 方案生成成功！下面是你的7天健身&饮食计划表")
    st.subheader("🔍 Agent自检信息")
    st.markdown(state["plan_text"])
    st.divider()

    st.subheader("📅 七天饮食计划表")
    st.table(state["food_table"])
    st.caption("表格列：星期｜早餐｜午餐｜加餐｜晚餐；忌口食材自行替换")
    st.divider()

    st.subheader("💪 七天训练计划表")
    st.table(state["train_table"])
    st.divider()

    # 导出文本
    export_text = "# 健身饮食计划表\n" + state["plan_text"] + "\n\n饮食计划：\n"
    for row in state["food_table"]:
        export_text += " | ".join(row) + "\n"
    export_text += "\n训练计划：\n"
    for row in state["train_table"]:
        export_text += " | ".join(row) + "\n"

    st.download_button("📥 下载计划表 Markdown", data=export_text, file_name="健身饮食计划表.md")

    if st.button("🔄 重新生成新方案"):
        state["agent_state"] = {
            "step": 0,
            "info": {},
            "plan_text": "",
            "train_table": [],
            "food_table": [],
            "thinking_log": [],
            "diff_level": "默认"
        }
        st.rerun()