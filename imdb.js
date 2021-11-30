// to save the time, I didn't convert strings to numbers, and now it causes trouble in some cases
db.title.ratings.distinct('averageRating').forEach(function(x) {
  db.title.ratings.updateMany(
    { averageRating: x },
    { $set: { averageRating: Number(x) }
  });
});

db.title.ratings.distinct('numVotes').forEach(function(x) {
  db.title.ratings.updateMany(
    { numVotes: x },
    { $set: { numVotes: parseInt(x) }
  });
});

// title.ratings with a rating of 10
db.title.ratings.find({ averageRating: { $gte: 10 } }).count(); // returns 4040