;; File I/O stuffs

#lang racket

;; (define s (string \#A))
;; (string-append s (~a l #:max-width len))

;; (define in (call-with-input-file "/home/sriram/src/python/mail_try/maildir/1"
;; 	     (lambda (in)
;; 	       (define s (make-string 0 #\nul))
;; 	       (for ([l (in-lines in)])
;; 		    (cond [(regexp-match? #rx"(From|To|Subject)" l)
;; 			   (let ([str ""]))
;; 			   (string-copy str (string-copy (string-append l s)))
;; 			   (print str)
;; 			   (newline)]
;; 			  [else
;; 			   (print "No")
;; 			   (newline)])))))

(define in (open-input-file "../maildir/1" #:mode 'text))
(define s (make-string 0 #\nul))
(define t (string-append s (port->string in)))
(define (match-fix)
  (define s (regexp-match* #rx"From" t))
  (print s))

(match-fix)
