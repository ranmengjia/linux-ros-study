import cv2  # 导入 OpenCV 库

# ===== 步骤1：读取测试图片 =====
img = cv2.imread('/home/user/chapt4/1.jpg')
# img 是一个 numpy 数组，形状 (高, 宽, 3)，3 是 BGR 三通道
# 注意 OpenCV 读图默认是 BGR 顺序，不是 RGB
print(f'图片尺寸: {img.shape}')

# ===== 步骤2：转灰度图 =====
# Haar 算法基于亮度差判断，颜色信息没用，灰度图更轻更快
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(f'灰度图尺寸: {gray.shape}')

# ===== 步骤3：加载 Haar 分类器 =====
# 加载预训练好的人脸检测模型
detector = cv2.CascadeClassifier(
    '/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml'
)

# ===== 步骤4：执行人脸检测 =====
faces = detector.detectMultiScale(
    gray,               # 输入：灰度图
    scaleFactor=1.1,    # 每次缩放比例（检测不同大小的脸）
    minNeighbors=5,     # 重叠框合并阈值（越大越严）
    minSize=(30, 30)    # 最小脸尺寸（小于30x30的忽略）
)

# faces 是个二维数组，每行一张脸：[x, y, w, h]
print(f'检测到 {len(faces)} 张人脸')
for i, (x, y, w, h) in enumerate(faces):
    print(f'  第{i}张脸: x={x}, y={y}, w={w}, h={h}')

# ===== 步骤5：在原图上画框，保存结果 =====
for (x, y, w, h) in faces:
    cv2.rectangle(
        img,                # 在哪张图上画
        (x, y),             # 左上角
        (x + w, y + h),     # 右下角
        (0, 255, 0),        # 绿色（BGR格式）
        2                   # 线宽
    )

# 保存结果图
cv2.imwrite('/home/user/chapt4/result.jpg', img)
print('结果已保存到 /home/user/chapt4/result.jpg')