# Timing is...

Everything! As the phrase goes. As a freelancer and remote worker, I've
searched high and low for a good way to manage my time and balance competing
priorities. The more apps I try, the more I keep coming back to the
fundamentals. The calendar is an ancient technology perfected over the
centuries throughout the world. Most people use it to plan for the future but
it works equally well to track the past and by using the same calendar for
forward planning and backward tracking you can build a feedback loop to
develop a an intuition for how well you follow through on your plans and how
realistic your planning is in the first place. This practice builds a certain
self-awareness about your perception of the future. I call it a "proprioception
of mind". Just as you have a proprioceptive feedback loop for the location of
parts of your body you can build a temporal awareness of mental model of the
world.

The app, currently, allows Google Calendar users to authorize timingis to
access their calendar data using OAuth 2.0 through the Google Calendar API. The
first full use case is to create a .PDF invoice of their tracked time over a
period of their selection using custom keywords in various fields of the
calendar events to filter and aggregate them.

The program is intended to be as flexible as possible to allow the user to use
a strategy of their choosing to track time. This is a proof of concept app and
much work is yet to be done, so any feedback or suggestions would be greatly
appreciated.

## Get started

```
$ cd ./TimingIs-Flask/timingis/
$ pip install -r requirements.txt
$ python3 app.py
```

## Contributors

If you're interested in contributing or otherwise getting involved contact me
here on Github @eayoungs. There's still some non-trivial refactoring that needs
to be done to modularize the code. I've also started a
[Django version](https://github.com/eayoungs/TimingIs-Django) to allow for
faster development, so you might want to check that out as well.

## License

Licensed under the GNU Affero General Public License
