;; Define structure for holding the list of mail's received.
#lang racket

(require web-server/servlet
	 web-server/servlet-env
	 web-server/templates
	 net/mime)

(struct mail (from date subject))

(define mlist (list))

(define (create-mail-items list)
  (mail 
   (cdr (assoc 'from list))
   (cdr (assoc 'date list))
   (cdr (assoc 'sub list))
   ))

(define (extract s)
  (define slist (list))
  (map (lambda(i)
	 (set! slist (cons (cond [(regexp-match #rx"^From" i) (cons 'from i)]
				 [(regexp-match #rx"^Date" i) (cons 'date i)]
				 [(regexp-match #rx"^Subject" i) (cons 'sub i)]
				 [else (print "No")])
			   slist))) s)
  slist)

;; [::CleanUp::]
(define (process-dir path)
  (define l (list))
  (define listoffiles (directory-list path #:build? #t))
  (set! mlist (cons
	       (map (lambda(i) 
		      (set! l (extract (message-fields (mime-analyze (open-input-file i)))))
		      (set! l (filter (lambda(i) (cons? i)) l))
		      ;; (print l)
		      ;; (newline)
		      (create-mail-items l))
		    listoffiles)
	       mlist))
  (set! mlist (car mlist)))

(process-dir "/home/sriram/src/python/mail_try/maildir/")

(define (start request)
  (include-template "template/welcome.html")
  (construct-stuffs request mlist))

(define (beautify str typ)
  (cond [(regexp-match #rx"from" typ)
	 (if (pair? (regexp-match #rx"<[a-zA-Z@.]+>" str))
	     (set! str (car (regexp-match #rx"<[a-zA-Z@.-]+>" str)))
	     (set! str (regexp-replace #rx"[=?a-z]+-[0-9?a-z?]+" (string-replace str "\"" "") ""))
	     )
	 str]
	[(regexp-match #rx"sub" typ) 
	 (define len (string-length str))
	 (cond [(>= len 20) (set! str (string-append (string-trim (substring str 0 20)) "...."))]
	       [else str])
	 str]
	[(regexp-match #rx"date" typ) 
	 (set! str (string-trim (regexp-replace #rx"[+|-]+[0-9]+" str "")))
	 str]
	[else str (print str) str]
	))

(define (render-post i)
  `(div ((class "item"))
	(div ((class "from"))
	     (strong ,(beautify (string-join (cdr (string-split (mail-from i) ":"))) "from" )))
	(div ((class "subject"))
	     (strong ,(beautify (string-join (cdr (string-split (mail-subject i) ":"))) "sub")))
	(div ((class "date"))
	     (strong ,(beautify (string-join (cdr (string-split (mail-date i) ":"))) "date")))
	))
 
(define (construct-div mlist)
  `(div ((class "list_container"))
        ,@(map (lambda(i) (render-post i)) mlist)))

(define (construct-stuffs request mlist)
  (response/xexpr
   `(html 
     (head (title "Inbox")
	   (link ((rel "stylesheet")
		  (href "/style.css")
		  (type "text/css")
		  )))
     (body (( class "body" ))
	   (div ((class "title"))
		"MailServ Inbox")
	   ,(construct-div mlist)))))

; Function called on server start
(serve/servlet start
	       #:stateless? #t
	       #:port 8081
	       #:launch-browser? #f
	       #:listen-ip #f
	       #:servlet-path "/mail"
	       #:server-root-path "/home/sriram/src/python/mail_try/web/")

;; #:extra-files-paths (list (build-path "/home/sriram/src/python/mail_try/web/css/"))
;; Study
;; #:servlet-regexp #rx".")

;; Procedure to read maildir, read files and do stuffs
;; (define mb "hcoop")
;; (define tag "hcoop")
;; (define body "Test")
;; (define in-file (open-input-file "/home/sriram/src/python/mlistry/maildir/1.mime"))
;; (define t (mime-analyze in-file))
;; (define s (message-fields t))
;; (define mlist (list (mail mb tag (list-ref s 9) (list-ref s 10) (list-ref s 11) (list-ref s 7) body)))
;; (define mlist 
;;   (list (mail "sriram.max@gmail.com" 
;; 	      "hello@test.com" "today" )
;; 	(mail "sriram.max@gmail.com" 
;; 	      "hello@test.com" "today")
;; 	))


