;; Define structure for holding the list of mail's received.
#lang racket

(require web-server/servlet
	 web-server/servlet-env
	 web-server/templates
	 net/mime)

;; Config path, global declaration
(define conf-path "/home/sriram/src/python/mail_try/conf/config")
(define conf-list (list))

(define (extract-path str)
  (set! conf-list (cons (list-ref (string-split str " ") 7)
	conf-list)))

(define (dir-from-config)
  (define data (string))
  (define conf-data (list))
  (set! conf-data (string-split (file->string conf-path) "\n"))
  (map (lambda(i)
	 (cond [(regexp-match #rx"^det" i) (extract-path i)]
		[else (print "No")]
		)) conf-data))

(dir-from-config)

(struct mail (from date subject))

(define mlist (list))

(define (create-mail-items list)
  (mail 
   (cdr (assoc 'from list))
   (cdr (assoc 'date list))
   (cdr (assoc 'sub list))))

(define (extract s)
  (define slist (list))
  (map (lambda(i)
	 (set! slist (cons (cond [(regexp-match #rx"^From" i) (cons 'from i)]
				 [(regexp-match #rx"^Date" i) (cons 'date i)]
				 [(regexp-match #rx"^Subject" i) (cons 'sub i)]
				 [else (print "No")])
			   slist))) s) slist)

(define (extract-msg-body in)
  (define cnt-list (file->string in))
  (map (lambda(i)
	 (cond [(regexp-match #rx"[A-Za-za-zA-Z:]+" i) (print i)]
	       [else (print i)]
	       )
	 )(string-split cnt-list "\r\n")))

;; [::CleanUp::]
(define (process-dir path)
  (define l (list))
  (define listoffiles (directory-list path #:build? #t))
  (set! mlist (cons
	       (map (lambda(i) 
		      (define in (open-input-file i))
		      (set! l (extract (message-fields (mime-analyze in))))
		      (set! l (filter (lambda(i) (cons? i)) l))
		      ;; (extract-msg-body i)
		      (create-mail-items l))
		    listoffiles)
	       mlist))
  (set! mlist (car mlist)))

(define (start request)
  (map (lambda(i) 
	 ;; Move process-each-dir somewhere else. [::NeedToThink::], And m sleepy
	 (process-dir (string-append "/home/sriram/src/python/mail_try/maildir/" i))
	 ) conf-list)
  (construct-stuffs request mlist))

(define (beautify str typ)
  (cond [(regexp-match #rx"from" typ)
	 (if (pair? (regexp-match #rx"<[a-zA-Z@.]+>" str))
	     (set! str (car (regexp-match #rx"<[a-zA-Z@.-]+>" str)))
	     (set! str (regexp-replace #rx"[=?a-z]+-[0-9?a-z?]+" (string-replace str "\"" "") ""))
	     )
	 str]
	[(regexp-match #rx"sub" typ) 
	 (cond [(>= (string-length str) 40) (set! str (string-append (string-trim (substring str 0 40)) "...."))]
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
     (head (title "maBox")
	   (link ((rel "stylesheet")
		  (href "/style.css")
		  (type "text/css")
		  )))
     (body (( class "body" ))
	   (div ((class "title"))
		"PostBox")
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


