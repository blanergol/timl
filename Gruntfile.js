module.exports = function (grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        clean: {
            build: {
                src: ['static/dist/js/**', 'static/dist/css/**', 'static/dist/img']
            }
        },

        copy: {
            bootstrapCss: {
                src: 'node_modules/bootstrap/dist/css/bootstrap.min.css',
                dest: 'static/dist/css/lib/bootstrap.min.css'
            },
            bootstrap: {
                src: 'node_modules/bootstrap/dist/js/bootstrap.min.js',
                dest: 'static/dist/js/lib/bootstrap.min.js'
            },
            jquery: {
                src: 'node_modules/jquery/dist/jquery.min.js',
                dest: 'static/dist/js/lib/jquery.min.js'
            }
        },

        jshint: {
            all: ['static/dev/js/custom.js']
        },

        uglify: {
            custom: {
                files: {
                    'static/dist/js/custom.min.js': ['static/dev/js/custom.js']
                }
            }
        },

        cssmin: {
            cutom: {
                files: {
                    'static/dist/css/custom.min.css': ['static/dev/css/custom.css']
                }
            }
        },

        imagemin: {
            dynamic: {
                files: [{
                    expand: true,
                    cwd: 'static/dev/img',
                    src: ['*.{png,jpg,gif}'],
                    dest: 'static/dist/img'
                }]
            }
        },

        watch: {
            scripts: {
                files: 'static/dev/js/custom.js',
                tasks: ['jshint', 'uglify'],
            },
            css: {
                files: 'static/dev/css/custom.css',
                tasks: ['cssmin'],
            },
        }
    });
    grunt.loadNpmTasks('grunt-contrib-clean')
    grunt.loadNpmTasks('grunt-contrib-copy')
    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-cssmin');
    grunt.loadNpmTasks('grunt-contrib-imagemin');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['clean', 'copy', 'jshint', 'uglify', 'cssmin', 'imagemin']);
};