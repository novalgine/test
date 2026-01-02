
import sqlite3
conn = sqlite3.connect('viral_reels.db')
c = conn.cursor()
c.execute("UPDATE users SET onboarding_complete = 0, user_mode = NULL WHERE username = 'semih'")
conn.commit()
conn.close()
print("Reset complete")
