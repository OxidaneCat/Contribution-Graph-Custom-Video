import os
import glob
from datetime import datetime, timedelta
import requests
from PIL import Image
import Config #other file in the same directory

def GetYear(YearValue, CurrentYear, Today):
    January1 = datetime(YearValue, 1, 1)
    #Get the weekday of January 1st 0=Sunday 6=Saturday
    #https://www.geeksforgeeks.org/python/python-strftime-function
    January1WithDay = int(January1.strftime('%w'))

    StartDate = January1 - timedelta(days=January1WithDay) #Pushing so we can start on a Sunday
    
    if YearValue == CurrentYear:
        EndDate = Today
        #so we no need to fetch future dates
    else:
        December31 = datetime(YearValue, 12, 31)
        #Get the weekday of December 31st 0=Sunday 6=Saturday

        December31Wday = int( December31.strftime('%w'))
        #how many days we need to add to December 31st to reach the nearest Saturday
        DaysToSat = (6 - December31Wday) % 7

        EndDate = December31 + timedelta(days = DaysToSat)
    #https://github.com/marketplace/actions/get-current-time
    return StartDate.strftime("%Y-%m-%dT00:00:00Z"), EndDate.strftime("%Y-%m-%dT23:59:59Z")

def GetCalendarContributions(Username, Token):
    Grid = [[0 for _ in range(Config.Cols)] for _ in range(Config.Rows)]
    ValidGrid = [[False for _ in range(Config.Cols)] for _ in range(Config.Rows)]

    if not Username or not Token:
        print("Missing Github username or token in Config.py!")
        return Grid, ValidGrid

    Today = datetime.utcnow()
    CurrentYear = Today.year
    YearsToFetch = [CurrentYear, CurrentYear - 1, CurrentYear - 2, CurrentYear - 3]
    
    #transparent gap rows
    YearOffsets = {
        CurrentYear: 0,       # Rows 0 to 6
        CurrentYear - 1: 8,   # Rows 8 to 14
        CurrentYear - 2: 16,  # Rows 16 to 22
        CurrentYear - 3: 24   # Rows 24 to 30
    }
    #https://medium.com/@yuichkun/how-to-retrieve-contribution-graph-data-from-the-github-api-dc3a151b4af
    #https://docs.github.com/en/graphql/reference/users
    Query = """
    query($user:String!, $from:DateTime, $to:DateTime) { 
        user(login: $user){
            contributionsCollection(from: $from, to: $to) {
                contributionCalendar {
                    weeks {
                        contributionDays {
                            contributionCount
                            date
                        }
                    }
                }
            }
        }
    }
    """
    Headers = {"Authorization": f"Bearer {Token}"}

    for YearValue in YearsToFetch: #4 years
        StartDate, EndDate = GetYear(YearValue, CurrentYear, Today)
        Variables = {
            "user": Username,
            "from": StartDate,
            "to": EndDate
        }
        
        try:
            print(f"STEALING contribution data for year {YearValue} ... lol")
            Response = requests.post("https://api.github.com/graphql", json={'query': Query, 'variables': Variables}, headers = Headers)
            Data = Response.json()
            
            if "errors" in Data:
                print(f"Warning for {YearValue} (Account might be newer)")
                continue
                
            # Extract the weeks data from the response
            Weeks = Data['data']['user']['contributionsCollection']['contributionCalendar']['weeks']

            #Map the contribution
            BaseRow = YearOffsets[YearValue]
            for ColIdx, Week in enumerate(Weeks):
                if ColIdx >= Config.Cols:
                    break
                for Day in Week['contributionDays']:
                    DayDate = datetime.strptime(Day['date'], "%Y-%m-%d")
                    
                    DayOfWeek = int(DayDate.strftime('%w'))
                    TargetRow = BaseRow + DayOfWeek
                    
                    if TargetRow < Config.Rows and ColIdx < Config.Cols:
                        Grid[TargetRow][ColIdx] = Day['contributionCount']
                        ValidGrid[TargetRow][ColIdx] = True  # Mark this cell as an active calendar day
        
        #crash                
        except Exception as E:
            print(f"Connection Exception for {YearValue}: {E}")
            
    print("Successfully stealing all yo contribution data")
    return Grid, ValidGrid
    #got the data

#render the APNG
def GenerateAPNG():
    print("Starting render layout...")
    UserGrid, ValidGrid = GetCalendarContributions(Config.GithubUsername, Config.GithubToken)
    #sort the frames in the Frames
    FrameFiles = sorted(glob.glob(os.path.join(Config.FramesDir, "*.png")))
    if not FrameFiles:
        print("No frames found")
        return

    ProcessedFrames = []
    print(f"Putting contribution data with {len(FrameFiles)} frames...") #total

    for File in FrameFiles:
        Img = Image.open(File).convert("L")
        Img = Img.resize((Config.Cols, Config.Rows), Image.Resampling.NEAREST)
        
        Canvas = Image.new("RGBA", (Config.Cols * Config.Scale, Config.Rows * Config.Scale), (0, 0, 0, 0))
        
        for Y in range(Config.Rows):
            if Y in [7, 15, 23]:
                continue

            for X in range(Config.Cols):
                if not ValidGrid[Y][X]:
                    continue

                VideoPixel = Img.getpixel((X, Y))
                DidContribute = UserGrid[Y][X] > 0
                
                if not DidContribute:
                    if VideoPixel > 128:
                        Color = Config.ColorWhite
                    else:
                        Color = Config.ColorBlack
                else:
                    if VideoPixel > 128:
                        Color = Config.ColorLightGreen
                    else:
                        Color = Config.ColorDarkGreen

                for Dx in range(Config.Scale - 1):
                    for Dy in range(Config.Scale - 1):
                        Canvas.putpixel((X * Config.Scale + Dx, Y * Config.Scale + Dy), Color)
                                
        ProcessedFrames.append(Canvas)

    print(f"Exporting {Config.OutputApng}...")
    ProcessedFrames[0].save(Config.OutputApng, save_all=True, append_images=ProcessedFrames[1:], duration=80, loop=0, format="PNG")
    print("Successfully exported APNG")

if __name__ == "__main__":
    GenerateAPNG()
