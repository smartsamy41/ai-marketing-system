from datetime import datetime

import time

from engine.master_engine import run_master_engine



# =========================

# ⏱️ SCHEDULER ENGINE V1

# =========================



def run_scheduler(interval_minutes=15):



    print("🟢 Scheduler started")

    print(f"⏱️ Interval: {interval_minutes} minutes")



    while True:



        try:



            print("\n🚀 RUNNING MASTER ENGINE:", datetime.now())



            result = run_master_engine()



            print("✅ EXECUTION DONE")

            print("STATUS:", result.get("status"))



        except Exception as e:



            print("❌ Scheduler Error:", str(e))



        # =========================

        # WAIT

        # =========================

        time.sleep(interval_minutes * 60)
