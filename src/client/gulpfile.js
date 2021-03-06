var gulp = require('gulp');


gulp.task('copy-index-html', function() {
    gulp.src('./index.html')
    .pipe(gulp.dest('../server/static'));
});

gulp.task('default', function(){
    gulp.start('copy-index-html');
});

gulp.task('watch', ['default'], function(){
    gulp.watch('./index.html', ['copy-index-html']);
});
