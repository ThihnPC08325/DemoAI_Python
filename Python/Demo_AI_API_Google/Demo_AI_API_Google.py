import os
import google.generativeai as genai
from datetime import datetime
from transformers import pipeline

# Lấy API key từ biến môi trường
API_KEY = "AIzaSyBR30tZcgmCwnRjNBXYsM14jKRQiRK9Bg8"
if not API_KEY:
    raise ValueError(
        "API key không được cung cấp. Vui lòng thiết lập biến môi trường API_KEY."
    )

# Cấu hình thư viện Generative AI
genai.configure(api_key=API_KEY)


# Hàm khởi tạo model
def setup_google_model():
    # Cấu hình tạo nội dung
    generation_config = {
        "temperature": 0.7,  # Thử nghiệm với giá trị cao hơn để tăng tính sáng tạo
        "top_p": 0.95,  # Mở rộng vùng xác suất
        "top_k": 50,  # Tăng số lượng token để lựa chọn
        "max_output_tokens": 2048,  # Duy trì số token tối đa
    }

    # Thiết lập cài đặt an toàn
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
        {
            "category": "HARM_CATEGORY_HATE_SPEECH",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
        # {
        #     "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        #     "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        # },
        {
            "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
            "threshold": "BLOCK_MEDIUM_AND_ABOVE",
        },
    ]

    # Khởi tạo model
    return genai.GenerativeModel(
        model_name="gemini-pro",
        generation_config=generation_config,
        safety_settings=safety_settings,
    )


# Hàm ghi lịch sử hội thoại
def log_conversation(user_input, ai_response, model_source):
    with open("chat_history.log", "a", encoding="utf-8") as log_file:
        log_file.write(f"[{datetime.now()}] Người dùng: {user_input}\n")
        log_file.write(f"[{datetime.now()}] AI ({model_source}): {ai_response}\n\n")


# Hàm gọi Google Generative AI
def generate_google_response(model, prompt_parts):
    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        print(f"Lỗi khi gọi Google Generative AI API: {e}")
        return None


# Hàm gọi Hugging Face Transformers
def generate_transformers_response(prompt):
    try:
        transformer_pipeline = pipeline("text-generation", model="gpt-2")
        response = transformer_pipeline(
            prompt, max_length=100, do_sample=True, temperature=0.7
        )
        return response[0]["generated_text"]
    except Exception as e:
        print(f"Lỗi khi gọi Hugging Face Transformers: {e}")
        return None


if __name__ == "__main__":
    # Khởi tạo mô hình Google Generative AI
    google_model = setup_google_model()


    conversation_history = []
    print("Chào mừng bạn đến với AI trò chuyện! Nhập 'exit' để kết thúc.")

    while True:
        user_input = input("Bạn: ")
        if user_input.lower() == "exit":
            print("Cảm ơn bạn đã trò chuyện! Hẹn gặp lại.")
            break

        # Tổng hợp ngữ cảnh hội thoại
        conversation_history.append(f"Người dùng: {user_input}")
        prompt_parts = "\n".join(conversation_history)

        # Chọn mô hình phản hồi
        print(
            "Chọn mô hình phản hồi: 1 - Google Generative AI, 2 - Hugging Face Transformers"
        )
        model_choice = input("Lựa chọn của bạn (1/2): ")

        if model_choice == "1":
            ai_response = generate_google_response(google_model, [prompt_parts])
            model_source = "Google Generative AI"
        elif model_choice == "2":
            ai_response = generate_transformers_response(prompt_parts)
            model_source = "Hugging Face Transformers"
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            continue

        if ai_response:
            print(f"AI ({model_source}): {ai_response}")
            conversation_history.append(f"AI: {ai_response}")

            # Lưu hội thoại vào log
            log_conversation(user_input, ai_response, model_source)

            # Thu thập phản hồi từ người dùng
            feedback = input("Bạn có hài lòng với câu trả lời này không? (yes/no): ")
            with open("feedback.log", "a", encoding="utf-8") as feedback_file:
                feedback_file.write(
                    f"[{datetime.now()}] Phản hồi ({model_source}): {feedback}\n"
                )
        else:
            print("AI gặp lỗi khi trả lời. Vui lòng thử lại.")
