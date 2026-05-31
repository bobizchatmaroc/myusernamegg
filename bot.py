import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

# ==========================================
# ⚙️ إعدادات البوت (تعديل الأدمين والتوكن)
# ==========================================
# ⚠️ 1. حط التوكن الجديد والمحمي ديالك هنا (من عند BotFather) ف بلاصة هاد الكتابة
TOKEN = "8979100283:AAEqamTdQ4kyELUrPtHKUDhx9HayWXUYzbw"

# ⚠️ 2. حط الأيدي (ID) الرقمي ديال حسابك هنا ف بلاصة 123456789 (تقدر تجيبه من بوت @userinfobot)
ADMIN_ID = 7670195186  

# حساب الدعم الرسمي الخاص بك الذي حددته
SUPPORT_USERNAME = "myusernamsgg"

# ⚠️ 3. الرابط اللي غاتعطيه ليك منصة Render الفابور غاتحطو هنا بعدين ليشتغل الـ WebApp
BASE_URL = "https://your-render-app-link.onrender.com" 

bot = Bot(token=TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)

# ==========================================
# 🌐 واجهة الماركت بليس (HTML/CSS/JS) فوتوكوبي
# ==========================================
HTML_TEMPLATE = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MyusernameGG - Marketplace</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }}
        body {{ background-color: #f4f6f9; color: #111; padding-bottom: 75px; }}
        
        /* الهيدر الأزرق فوتوكوبي */
        .hero-banner {{
            background: linear-gradient(135deg, #007aff, #0040c7); color: white;
            padding: 30px 20px; border-bottom-left-radius: 25px; border-bottom-right-radius: 25px;
        }}
        .badge-update {{ background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 12px; font-size: 11px; font-weight: bold; display: inline-block; margin-bottom: 10px; }}
        .hero-banner h1 {{ font-size: 24px; margin-bottom: 5px; }}
        .hero-banner p {{ font-size: 13px; opacity: 0.9; }}

        /* بنر التوثيق بـ 49$ */
        .verification-banner {{
            background: #000; color: white; margin: 15px; padding: 15px; border-radius: 20px;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .verification-banner p {{ font-size: 14px; font-weight: bold; }}
        .verification-btn {{ background: white; color: black; border: none; padding: 10px 20px; border-radius: 20px; font-weight: bold; cursor: pointer; }}

        /* قائمة عرض اليوزرات */
        .market-container {{ padding: 0 15px; display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        .user-card {{ background: white; padding: 20px; border-radius: 20px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.03); border: 1px solid #eee; }}
        .user-card h3 {{ font-size: 18px; margin-bottom: 8px; color: #000; font-weight: 800; }}
        .user-card .price {{ color: #007aff; font-weight: bold; font-size: 14px; }}

        /* لوحة تتبع الأوردر والوسيط Escrow */
        .escrow-box {{ background: white; margin: 15px; padding: 20px; border-radius: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }}
        .timeline-step {{ display: flex; align-items: flex-start; margin-bottom: 20px; position: relative; }}
        .step-icon {{ width: 24px; height: 24px; border-radius: 50%; background: #ddd; display: flex; align-items: center; justify-content: center; font-size: 12px; margin-right: 15px; z-index: 2; }}
        .step-icon.active {{ background: #34c759; color: white; }}
        .step-info h4 {{ font-size: 14px; color: #000; }}
        .step-info p {{ font-size: 12px; color: #8e8e93; }}

        /* البار السفلي للتنقل */
        .nav-bar {{
            position: fixed; bottom: 0; left: 0; right: 0; height: 70px; background: white;
            display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #eee;
        }}
        .nav-item {{ text-align: center; color: #8e8e93; font-size: 12px; cursor: pointer; flex: 1; padding: 10px 0; }}
        .nav-item.active {{ color: #007aff; font-weight: bold; }}
        .nav-item span {{ display: block; font-size: 20px; margin-bottom: 3px; }}

        .view-section {{ display: none; }}
        .view-section.active {{ display: block; }}
    </style>
</head>
<body>

    <div id="home-view" class="view-section active">
        <div class="hero-banner">
            <span class="badge-update">UPDATE V3.1 • OUT NOW</span>
            <h1>Welcome to MyusernameGG</h1>
            <p>Buy & sell rare usernames with escrow protection.</p>
        </div>

        <div class="verification-banner">
            <div>
                <p style="font-size: 12px; opacity: 0.6; font-weight: normal;">Featured Service ✨</p>
                <p>Verify account for $49</p>
            </div>
            <button class="verification-btn" onclick="requestVerification()">Get it</button>
        </div>

        <p style="padding: 10px 20px; font-weight: bold; color: #8e8e93;">1,081 listings available</p>
        <div class="market-container">
            <div class="user-card"><h3>@qviaw</h3><p class="price">2.84 TON</p></div>
            <div class="user-card"><h3>@bitgettoken</h3><p class="price">15.00 TON</p></div>
        </div>
    </div>

    <div id="sell-view" class="view-section" style="padding: 20px;">
        <h2 style="margin-bottom: 20px;">Sell Username</h2>
        <p style="color: #666; margin-bottom: 15px;">حط اليوزر ديالك والثمن باش تشريه، وغادي يتصيفط للأدمين للمراجعة والموافقة:</p>
        <input type="text" id="username_input" placeholder="@username" style="width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #ccc; margin-bottom: 15px; font-size: 16px;">
        <input type="number" id="price_input" placeholder="Price in TON" style="width: 100%; padding: 15px; border-radius: 12px; border: 1px solid #ccc; margin-bottom: 20px; font-size: 16px;">
        <button style="width: 100%; background: #007aff; color: white; border: none; padding: 15px; border-radius: 12px; font-weight: bold; font-size: 16px;" onclick="submitListing()">Submit to Review</button>
    </div>

    <div id="orders-view" class="view-section">
        <h3 style="padding: 20px 20px 5px 20px;">Escrow Timeline</h3>
        <div class="escrow-box">
            <div style="display: flex; justify-content: space-between; margin-bottom: 20px; font-weight: bold;">
                <span>x8rz1</span> <span style="color: #007aff;">2.8409 TON</span>
            </div>
            <div class="timeline-step">
                <div class="step-icon active">✓</div>
                <div class="step-info"><h4>Payment secured</h4><p>Buyer paid. Start delivery.</p></div>
            </div>
            <div class="timeline-step">
                <div class="step-icon active">✓</div>
                <div class="step-info"><h4>Seller delivering <span style="color: #34c759; font-size: 11px;">Now</span></h4><p>Upload proof when handover is ready.</p></div>
            </div>
            <div class="timeline-step">
                <div class="step-icon">○</div>
                <div class="step-info"><h4>Buyer confirms</h4><p>Waiting for buyer confirmation.</p></div>
            </div>
        </div>
    </div>

    <div class="nav-bar">
        <div id="nav-home" class="nav-item active" onclick="switchView('home')"><span>🏠</span>Home</div>
        <div id="nav-sell" class="nav-item" onclick="switchView('sell')"><span>➕</span>Sell</div>
        <div id="nav-orders" class="nav-item" onclick="switchView('orders')"><span>📋</span>Orders</div>
    </div>

    <script>
        window.Telegram.WebApp.ready();
        window.Telegram.WebApp.expand();

        function switchView(viewName) {{
            document.querySelectorAll('.view-section').forEach(view => view.classList.remove('active'));
            document.querySelectorAll('.nav-item').forEach(item => item.classList.remove('active'));
            document.getElementById(viewName + '-view').classList.add('active');
            document.getElementById('nav-' + viewName).classList.add('active');
        }}

        function submitListing() {{
            const user = document.getElementById('username_input').value;
            const price = document.getElementById('price_input').value;
            if(!user || !price) {{ alert('عمر الخانات كاملين أولاً!'); return; }}
            
            window.Telegram.WebApp.sendData(JSON.stringify({{action: "sell_item", username: user, price: price}}));
            window.Telegram.WebApp.close();
        }}

        function requestVerification() {{
            window.Telegram.WebApp.showPopup({{
                title: 'Verification Request',
                message: 'هل تريد توثيق حسابك والحصول على الشارة الزرقاء مقابل 49$؟',
                buttons: [{{id: 'ok', type: 'default', text: 'نعم، شراء'}}]
            }}, function(buttonId) {{
                if(buttonId === 'ok') {{
                    window.Telegram.WebApp.sendData(JSON.stringify({{action: "buy_verification", price: 49}}));
                }}
            }});
        }}
    </script>
</body>
</html>
"""

# ==========================================
# 🤖 محرك البوت والإشعارات والدعم (Backend)
# ==========================================

# أمر البداية /start لوحة تحكم البوت
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📱 Open MyusernameGG", web_app=WebAppInfo(url=BASE_URL)))
    builder.row(InlineKeyboardButton(text="💬 Contact Support (الدعم)", url=f"https://t.me/{SUPPORT_USERNAME}"))
    
    await message.reply(
        "Welcome to **MyusernameGG** 🚀\n"
        "The ultimate marketplace to buy & sell rare usernames with escrow protection.\n\n"
        "اضغط على الزر أسفله لفتح الماركت بليس مباشرة👇",
        reply_markup=builder.as_markup(),
        parse_mode="Markdown"
    )

# استقبال البيانات القادمة من واجهة الـ Webapp
@dp.message(lambda msg: msg.web_app_data is not None)
async def webapp_data_receive(message: types.Message):
    data = json.loads(message.web_app_data.data)
    
    # 1. طلب بيع يوزر من الواجهة
    if data.get("action") == "sell_item":
        username = data.get("username")
        price = data.get("price")
        
        await message.reply("⏳ تم إرسال يوزرك للمراجعة. غاتوصلك رسالة هنا فور موافقة الإدارة.")
        
        builder = InlineKeyboardBuilder()
        builder.row(
            InlineKeyboardButton(text="✅ Approve", callback_data=f"app_{username}_{price}_{message.from_user.id}"),
            InlineKeyboardButton(text="❌ Reject", callback_data=f"rej_{username}_{message.from_user.id}")
        )
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=f"🔔 **طلب بيع جديد ينظر موافقتك:**\n\n📦 اليوزر: {username}\n💰 الثمن: {price} TON\n👤 البائع: {message.from_user.id}",
            reply_markup=builder.as_markup()
        )
        
    # 2. طلب التوثيق بـ 49$
    elif data.get("action") == "buy_verification":
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="💬 تواصل مع الدعم الفني", url=f"https://t.me/{SUPPORT_USERNAME}"))
        
        await message.reply(
            "💸 **تم تسجيل طلب التوثيق بقيمة 49$**\n\nاضغط على الزر أسفله للتواصل مباشرة مع المطور لإتمام الدفع وتفعيل الشارة الزرقاء على حسابك الحقيقي.", 
            reply_markup=builder.as_markup()
        )
        # إشعار للأدمين (أنت)
        await bot.send_message(
            chat_id=ADMIN_ID,
            text=f"✨ **طلب توثيق جديد ($49):**\n👤 المستخدم: {message.from_user.full_name} (`{message.from_user.id}`)\nUsername: @{message.from_user.username or 'لا يوجد'}"
        )

# معالجة أزرار الأدمين (موافقة / رفض وعمل الإشعارات)
@dp.callback_query(lambda c: c.data.startswith(("app_", "rej_")))
async def admin_decision(callback: types.CallbackQuery):
    parts = callback.data.split("_")
    action = parts[0]
    username = parts[1]
    
    if action == "app":
        price = parts[2]
        seller_id = int(parts[3])
        await callback.message.edit_text(text=f"✅ تمت الموافقة على اليوزر {username} وتم نشره.")
        
        # إرسال إشعار فوتوكوبي للبيع الناجح للمستخدم
        order_text = (
            "🏆 **Order Completed!**\n\n"
            "The order has been completed successfully:\n"
            "📦 `{}`\n"
            "🔢 Order: MUG-01603\n\n"
            "Thank you for using our marketplace!"
        ).format(username)
        await bot.send_message(chat_id=seller_id, text=order_text, parse_mode="Markdown")
    else:
        seller_id = int(parts[2])
        await callback.message.edit_text(text=f"❌ تم رفض طلب {username}.")
        await bot.send_message(chat_id=seller_id, text=f"⚠️ نعتذر منك، تم رفض عرض يوزرك {username} من طرف الإدارة.")
    await callback.answer()

# سيستم تحويل رسائل الدعم في الشات العادي إليك
@dp.callback_query(lambda c: c.data == "contact_support")
async def support_handler(callback: types.CallbackQuery):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💬 اذهب للدعم المباشر", url=f"https://t.me/{SUPPORT_USERNAME}"))
    await callback.message.answer("لحل أي مشاكل أو استفسارات، يرجى مراسلة المطور مباشرة بالضغط على الزر أسفله:", reply_markup=builder.as_markup())
    await callback.answer()

@dp.message()
async def forward_to_admin(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        builder = InlineKeyboardBuilder()
        builder.row(InlineKeyboardButton(text="💬 مراسلة المطور", url=f"https://t.me/{SUPPORT_USERNAME}"))
        await message.reply("✅ لحل المشاكل التقنية أو معالجة المعاملات، يرجى مراسلة حساب الدعم الخاص بنا مباشرة:", reply_markup=builder.as_markup())

# ==========================================
# 🌍 خادم الويب المدمج لخدمة الـ WebApp فابور
# ==========================================
async def handle_webapp(request):
    return web.Response(text=HTML_TEMPLATE, content_type='text/html')

async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    import asyncio
    asyncio.create_task(dp.start_polling(bot))

def main():
    app = web.Application()
    app.router.add_get('/', handle_webapp)
    app.on_startup.append(on_startup)
    web.run_app(app, host='0.0.0.0', port=10000)

if __name__ == '__main__':
    main()
