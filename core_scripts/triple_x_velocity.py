import asyncio
import time
import random

async def cognitive_pulse(task_id, speed_mode="LIGHTSPEED"):
    """
    จำลองการทำงานของ AI แต่ละ Task 
    """
    # ถ้าเป็น LIGHTSPEED จะสุ่มรอ 0.1 - 0.5 วินาที (เร็วมาก)
    # ถ้าโหมดปกติจะสุ่มรอ 1.0 - 3.0 วินาที
    delay = random.uniform(0.1, 0.5) if speed_mode == "LIGHTSPEED" else random.uniform(1.0, 3.0)
    
    await asyncio.sleep(delay) # จำลอง I/O Bound task
    return f"⚡ Task {task_id:02d} Completed in {delay:.4f}s"

async def activate_triple_x_mode():
    print(f"\n{'='*50}")
    print(f"🚀 Initiating TRIPLE-X Speed Protocol...")
    print(f"{'='*50}\n")
    
    start_time = time.perf_counter() # ใช้ perf_counter จะแม่นยำกว่าสำหรับจับเวลา code

    # 1. สร้าง List ของ Tasks (ยังไม่รันทันที)
    task_count = 50
    tasks = [cognitive_pulse(i, speed_mode="LIGHTSPEED") for i in range(task_count)]

    # 2. สั่งประมวลผลพร้อมกัน (Concurrent Execution)
    # asyncio.gather จะรันทุกอย่างใน Event Loop เดียวกันแบบสลับกันทำงานอัตโนมัติ
    results = await asyncio.gather(*tasks)

    end_time = time.perf_counter()
    total_time = end_time - start_time

    # 3. แสดงผลลัพธ์
    for res in results[:5]: # สุ่มโชว์ 5 อันแรกเพื่อไม่ให้รกหน้าจอ
        print(res)
    print("...")
    
    print(f"\n{'-'*50}")
    print(f"✅ Processed {len(results)} cognitive tasks.")
    print(f"⏱️ Total Execution Time: {total_time:.4f} seconds")
    
    # คำนวณความเร็วที่เพิ่มขึ้น (เทียบกับถ้าต้องรันทีละอันแบบ Linear)
    # สมมติว่าถ้าทำงานปกติจะใช้เวลาเฉลี่ย 2 วินาทีต่อ 1 งาน
    estimated_linear_time = task_count * 2.0
    efficiency = estimated_linear_time / total_time
    print(f"💡 Efficiency Gain: {efficiency:.1f}x faster than linear processing")
    print(f"{'-'*50}\n")

if __name__ == "__main__":
    try:
        # วิธีมาตรฐานในการรัน Async function ใน Python 3.7+
        asyncio.run(activate_triple_x_mode())
    except KeyboardInterrupt:
        print("\n⚠️ Protocol terminated by user.")