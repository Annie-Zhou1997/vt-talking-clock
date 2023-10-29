# Vt-talking-clock :diamond_shape_with_a_dot_inside:
## Project description
This is the README for our group project.
## Requirements before installing
python
## Installation
123
## Supported Languages
- English :globe_with_meridians:
- Dutch :netherlands:
- Russian :ru:
- Mandarin :cn:
## Fuctions
Time zone selection

Theme control
- change the face of clock when click the 'Theme' button

## Usage
123
### Required Libraries

- **PyQt6**:
    ```bash
    pip install PyQt6
    ```
- **pytz**:
    ```bash
    pip install pytz
    ```
- **gTTS** (Google Text-to-Speech):
    ```bash
    pip install gTTS
    ```
- **playsound**:
    ```bash
    pip install playsound
    ```
- **python-dateutil**:
    ```bash
    pip install python-dateutil
    ```
- **tzlocal**:
    ```bash
    pip install tzlocal
    ```
## Group Members
- Igor Marchenko
- Youyang Cai
- Wangyiyao (Annie) Zhou
- Yanpei (Page) Ouyang
- Yi Lei
   
# Linguistic rules for telling time
## Russian :ru:
Russian 
## 汉语时间表达规则 (Chinese Mandarin Time Expression) :cn:
In Chinese, the formant of telling time is:
``"The current time is" + hour + "point" + minutes/"half"/"o'clock" + 'minutes'(or not)``
### 整点报时 (On the Hour)
当分钟为 `00` 时，我们直接说小时。

When the minutes are `00`, we directly say the hour.

- 3:00: "三点整" ("Three o'clock")
- 8:00: "八点整" ("Eight o'clock")

### 半点 (Half Past)
当分钟为 `30` 时，我们使用“半”这个词。

When the minutes are `30`, we use the word "半" (half).

- 3:30: "三点半" ("Half past three")
- 8:30: "八点半" ("Half past eight")

### 刻钟 (Quarter Hour)
刻钟通常是指15分钟的一个时间段。我们通常会用“一刻”、“两刻”和“三刻”来表示。

A quarter hour usually refers to a 15-minute period. We often use "一刻" (one quarter), "两刻" (two quarters), and "三刻" (three quarters) to express this.

- 3:15: "三点一刻" 或 "三点十五" ("A quarter past three" or "Three fifteen")
- 3:45: "三点三刻" 或 "四点差一刻" ("A quarter to four" or "Three forty-five")

### 具体分钟 (Specific Minutes)
对于 `01` 到 `29` 和 `31` 到 `59` 分钟的时间，我们通常直接说出具体的分钟数。

For times between `01` to `29` and `31` to `59` minutes, we usually say the specific number of minutes.

- 3:05: "三点零五" 或 "三点五分" ("Three oh five" or "Three five")
- 8:20: "八点二十" ("Eight twenty")

### 上午和下午 (AM and PM)
汉语中一般使用“上午”、“中午”和“下午”来区分时间段。

In Chinese, we generally use "上午" (morning), "中午" (noon), and "下午" (afternoon) to distinguish different parts of the day.

- 3:00 AM: "上午三点" ("Three o'clock in the morning")
- 3:00 PM: "下午三点" ("Three o'clock in the afternoon")
- 12:00 PM: "中午十二点" ("Twelve o'clock at noon")

### 总结 (Conclusion)
这些是一些基本的汉语报时方式和用法。不同地区和不同个人的习惯可能会有所不同，但这些是最常见和广泛接受的表达方式。

These are some basic ways and usages of telling time in Chinese. Habits may vary by region and individual, but these are the most common and widely accepted expressions.

:high_brightness:然而，在我们的项目中，我们没有采用过于复杂的汉语时间表达方式。千禧年后，普通话母语者很少使用“一刻”这个词

:high_brightness:However, in our project, we have not adopted overly complex Chinese time expressions. After the millennium, native Chinese speakers rarely say "一刻"(Quarter) in Mandarin.

## English Time Expressions :globe_with_meridians:
### On the Hour
When the minutes are `00`, we use the phrase "o'clock". 

- 3:00: "It's three o'clock."
- 8:00: "It's eight o'clock."

### Half Past
When the minutes are `30`, we use the phrase "half past".

- 3:30: "It's half past three."
- 8:30: "It's half past eight."

### Quarter Past
When the minutes are `15`, we use the phrase "quarter past".

- 3:15: "It's quarter past three."
- 8:15: "It's quarter past eight."

### Quarter To
When the minutes are `45`, we use the phrase "quarter to" for the next hour.

- 2:45: "It's quarter to three."
- 7:45: "It's quarter to eight."

### Minutes Past
For times between `01` and `29` minutes past the hour, we say the number of minutes after "past".

- 3:05: "It's five past three."
- 8:20: "It's twenty past eight."

### Minutes To
For times between `31` and `59` minutes past the hour, we say the number of minutes before "to" the next hour.

- 2:50: "It's ten to three."
- 7:40: "It's twenty to eight."

### AM and PM
To distinguish between morning and afternoon/evening, we use "AM" for times from midnight to just before noon, and "PM" for times from noon to just before midnight.

- 3:00 AM: "It's three o'clock in the morning."
- 3:00 PM: "It's three o'clock in the afternoon."
  
### Note :bulb:
Due to very limited time, we have only adopted expressions such as "On the Hour," "Half Past," "Quarter Past," and "Quarter To."
# GDPR Compliance

The recordings in this project are provided by members of our team. The voice for Chinese is from Youyang Cai, for Russian, it's Igor Marchenko, and for English, it's Annie Zhou. Dutch speech synthesis was generated using Google's [gTTS](https://gtts.readthedocs.io/en/latest/license.html). Therefore, the clock data in this project complies with GDPR regulations.
