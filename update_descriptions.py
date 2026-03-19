"""
update_descriptions.py — Load long descriptions into the database

Run once:
    python3 update_descriptions.py

To update a description later, edit the text below and run again.
"""

from app import app
from models import db, Trail

DESCRIPTIONS = {
    "Salem Lake Trail": (
        "The Salem Lake Trail is a seven-mile loop on hard-packed doubletrack that follows the "
        "perimeter of Salem Lake. The trail connects to the Salem Creek Greenway which leads into "
        "downtown Winston-Salem. There are multiple parking areas with access to the trail. Overall, "
        "this loop is great for an easier ride or when local trails are too wet to ride."
    ),
    "Salem Lake North Side": (
        "This is the main route through the trails on the north side of Salem Lake. These trails are "
        "not maintained and there are a lot of side loop trails. This main route is well worn and has "
        "a good flow. Pick up the trail entrance off the entrance road of New Greensboro Road. There "
        "is a parking lot at the gate and just head down the road to the trail entrance on the left "
        "side. There are a lot of log crossings on the trail, most are ramped or have bypasses. The "
        "singletrack eventually dumps you out on the doubletrack around Salem Lake and you take it "
        "back to the start. You can also go the long way around the lake on the doubletrack trail."
    ),
    "Hobby Park": (
        "Hobby Park is aerobically challenging and a perennial course of several mountain bike race "
        "series. The trail starts playfully, with several bumps, rocks, manmade mounds, and roots to "
        "be jumped. The trail then drops significantly to give the rider as much downhill speed as can "
        "be controlled. You'll descend football field-length falls and pedal up climbs for almost as "
        "long to get to the bottom of the park and the soapbox derby run for the ascent to the top on "
        "the other side. The ability to carry speed will reward the rider with a needed upward boost "
        "on climbs that will drive most riders to their aerobic capacity. Not anticipating the correct "
        "trail flow can put one high or low into the curve and result in some hike-a-bike. As the "
        "bottom is approached, rocks become a factor as the trail changes from clay to sand and "
        "pebble. The descents are left behind and the ascent begins up and around pebbles, baby heads "
        "and boulders. Just before crossing the small lakes to the right is the optional trail called "
        "Little Pisgah, a half-mile diversion that evokes visions of its Western mountain namesake. "
        "Continue the climb that offers variety to the other side, mostly ascending rocky terrain or "
        "grass over clay to the top, then cross the entrance road to Hobby and back to the parking lot."
    ),
    "The Ridge Cycle Hub": (
        "Enjoy 10.7 miles of singletrack mountain bike trail, providing intermediate to advanced "
        "bikers with rollercoaster drops and climbs. The gorgeous terrain gives riders the feel of "
        "Pisgah with the added City Lake views, and features great flow, rewarding climbs, and fun "
        "berms. The trail is one-way. The main loop covers 6.7 miles, with an optional 4-mile "
        "extension available for those looking to add more miles to their ride."
    ),
    "Back Yard Trails (BYT)": (
        "A technical gem in the heart of Charlotte, this ride has many unique and difficult features. "
        "The trails are slightly lacking in overall flow and get exponentially more difficult when wet. "
        "This ride caters more to the freeride/huckster than to the XC rider. "
        "These trails close for 24 hours after rain."
    ),
}


def update():
    with app.app_context():
        updated = 0
        for name, description in DESCRIPTIONS.items():
            trail = Trail.query.filter_by(name=name).first()
            if trail:
                trail.long_description = description
                updated += 1
            else:
                print(f"Warning: trail '{name}' not found in database")
        db.session.commit()
        print(f"Done — {updated} trail description(s) updated.")


if __name__ == "__main__":
    update()
