((nil . ((indent-tabs-mode . nil)
	 (c-basic-offset . 4)))
 (html-mode . ((sgml-basic-offset . 4)))
 (org-mode . ((org-publish-project-alist
	       . (("github-page"
		   :base-directory "~/proj/github.io/org"
		   :base-extension "org"
		   :publishing-directory "~/proj/github.io/"
		   :recursive t
		   :publishing-function org-html-publish-to-html
		   :headline-level 4
                   :with-toc nil
		   :body-only t ;; Only export section between <body> </body>
		   )
		  ("github-static"
		   :base-directory "~/proj/github.io/org"
		   :base-extension "css\\|js\\|png\\|jpg\\|gif\\|pdf\\|mp3\\|ogg\\|swf\\|stl"
		   :publishing-directory "~/proj/github.io/"
		   :recursive t
		   :publishing-function org-publish-attachment)
		  ("github" :components ("github-page" "github-static")))))))
