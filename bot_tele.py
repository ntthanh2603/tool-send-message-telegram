import telebot
import time

# Token khi tạo bot trong @BotFather
bot_token = "abcdxyz:123123123"
chat_id = "-4781733038"

# Khởi tạo bot
bot = telebot.TeleBot(bot_token)

# Danh sách các lỗi
error_list = [
    {"id": "e001", "description": "Lỗi kết nối cơ sở dữ liệu"},
    {"id": "e002", "description": "Lỗi xác thực người dùng"},
    {"id": "e003", "description": "Lỗi tải trang chủ"}
]

# Danh sách các lỗi đã sửa
success_list = []

# Danh sách các cảnh báo
warning_list = [
    {"id": "w001", "message": "Cảnh báo: Đừng gửi tin nhắn spam"},
    {"id": "w002", "message": "Cảnh báo: Không chia sẻ thông tin cá nhân"},
    {"id": "w003", "message": "Cảnh báo: Hãy tôn trọng các thành viên khác"}
]

# Thêm biến để lưu danh sách cảnh báo đã xử lý
warning_success_list = []

# Định dạng tin nhắn
def format_list(items, prefix=""):
    if not items:
        return "Danh sách trống."
    
    result = ""
    for item in items:
        if prefix == "Lỗi":
            result += f"🔴 {prefix} #{item['id']}: {item['description']}\n"
        elif prefix == "Đã sửa":
            result += f"✅ {prefix} #{item['id']}: {item['description']}\n"
        elif prefix == "Cảnh báo":
            result += f"⚠️ {prefix} #{item['id']}: {item['message']}\n"
    return result

# Xử lý lệnh /menu
@bot.message_handler(commands=['menu'])
def handle_menu(message):
    menu_text = """
🚀🚀🚀 Quản lý SNet 🚀🚀🚀

🔴 /error - Hiển thị danh sách lỗi
🔥 /adderror/id/content - Thêm lỗi mới
✅ /fixbug/{error_id} - Đánh dấu lỗi đã sửa
⚠️ /warn - Hiển thị danh sách cảnh báo
📝 /addwarning/id/content - Thêm cảnh báo mới
❌ /removewarning/{warning_id} - Đánh dấu cảnh báo đã xử lý
✨ /success - Hiển thị danh sách lỗi và cảnh báo đã xử lý
📜 /menu - Hiển thị menu này
"""
    bot.reply_to(message, menu_text)

# Xử lý lệnh /error
@bot.message_handler(commands=['error'])
def handle_error(message):
    error_message = "📋 DANH SÁCH LỖI\n\n"
    error_message += format_list(error_list, "Lỗi")
    bot.reply_to(message, error_message)

# Xử lý lệnh /fixbug
@bot.message_handler(func=lambda message: message.text.startswith('/fixbug/'))
def handle_fixbug(message):
    error_id = message.text[8:].strip()
    error_to_fix = None
    for error in error_list:
        if error['id'] == error_id:
            error_to_fix = error
            break
    
    if error_to_fix:
        error_list.remove(error_to_fix)
        success_list.append(error_to_fix)
        bot.reply_to(message, f"✅ Lỗi #{error_id} đã được đánh dấu là đã sửa thành công!")
    else:
        bot.reply_to(message, f"❌ Không tìm thấy lỗi có mã #{error_id}")

# Xử lý lệnh /success
@bot.message_handler(commands=['success'])
def handle_success(message):
    success_message = "📋 DANH SÁCH ĐÃ XỬ LÝ\n\n"
    if success_list:
        success_message += "🔧 LỖI ĐÃ SỬA:\n"
        success_message += format_list(success_list, "Đã sửa")
    if warning_success_list:
        success_message += "\n⚡ CẢNH BÁO ĐÃ XỬ LÝ:\n"
        success_message += format_list(warning_success_list, "Cảnh báo")
    if not success_list and not warning_success_list:
        success_message += "Chưa có lỗi hoặc cảnh báo nào được xử lý."
    bot.reply_to(message, success_message)

# Xử lý lệnh /warn
@bot.message_handler(commands=['warn'])
def handle_warning(message):
    warn_message = "⚠️ DANH SÁCH CẢNH BÁO\n\n"
    warn_message += format_list(warning_list, "Cảnh báo")
    bot.reply_to(message, warn_message)

# Xử lý lệnh /adderror
@bot.message_handler(func=lambda message: message.text.startswith('/adderror/'))
def handle_add_error(message):
    try:
        # Format: /adderror/e004/Description of the error
        parts = message.text[10:].split('/', 1)
        if len(parts) != 2:
            raise ValueError("Invalid format")
        
        error_id = parts[0].strip()
        description = parts[1].strip()
        
        if any(error['id'] == error_id for error in error_list):
            bot.reply_to(message, f"❌ Lỗi #{error_id} đã tồn tại!")
            return
        
        new_error = {"id": error_id, "description": description}
        error_list.append(new_error)
        bot.reply_to(message, f"✅ Đã thêm lỗi mới:\n🔴 Lỗi #{error_id}: {description}")
    except Exception as e:
        bot.reply_to(message, "❌ Format không hợp lệ. Sử dụng: /adderror/id/mô tả lỗi")

# Xử lý lệnh /addwarning
@bot.message_handler(func=lambda message: message.text.startswith('/addwarning/'))
def handle_add_warning(message):
    try:
        # Format: /addwarning/w004/Warning message
        parts = message.text[12:].split('/', 1)
        if len(parts) != 2:
            raise ValueError("Invalid format")
        
        warning_id = parts[0].strip()
        warning_msg = parts[1].strip()
        
        if any(warning['id'] == warning_id for warning in warning_list):
            bot.reply_to(message, f"❌ Cảnh báo #{warning_id} đã tồn tại!")
            return
        
        new_warning = {"id": warning_id, "message": warning_msg}
        warning_list.append(new_warning)
        bot.reply_to(message, f"✅ Đã thêm cảnh báo mới:\n⚠️ Cảnh báo #{warning_id}: {warning_msg}")
    except Exception as e:
        bot.reply_to(message, "❌ Format không hợp lệ. Sử dụng: /addwarning/id/nội dung cảnh báo")

# Thêm lệnh xóa cảnh báo
@bot.message_handler(func=lambda message: message.text.startswith('/removewarning/'))
def handle_remove_warning(message):
    warning_id = message.text[15:].strip()
    warning_to_remove = None
    
    for warning in warning_list:
        if warning['id'] == warning_id:
            warning_to_remove = warning
            break
    
    if warning_to_remove:
        warning_list.remove(warning_to_remove)
        warning_success_list.append(warning_to_remove)
        bot.reply_to(message, f"✅ Cảnh báo #{warning_id} đã được đánh dấu là đã xử lý!")
    else:
        bot.reply_to(message, f"❌ Không tìm thấy cảnh báo có mã #{warning_id}")

# Hàm main để chạy bot
def main():
    print("Bot đang khởi động...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print(f"Có lỗi xảy ra: {e}")
        time.sleep(15)
        main() 

if __name__ == "__main__":
    main()