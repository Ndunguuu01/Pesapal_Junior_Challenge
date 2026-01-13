from minidb import MiniDB
import sys

def run_repl():
    print("="*40)
    print("   PESAPAL CHALLENGE DB (v1.0)")
    print("   Type 'exit' to quit.")
    print("="*40)
    
    db = MiniDB()

    while True:
        try:
            # Get input
            user_input = input("SQL > ")
            if user_input.lower() in ['exit', 'quit']:
                break
            
            # Execute
            result = db.execute(user_input)
            
            # Display Result
            if isinstance(result, list):
                if len(result) == 0:
                    print("(0 rows)")
                else:
                    print(f"({len(result)} rows found)")
                    print("-" * 20)
                    for row in result:
                        print(row)
                    print("-" * 20)
            else:
                print(f"MSG: {result}")
                
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    run_repl()