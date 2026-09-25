(deftemplate record
   (slot record-id)
   (slot record-type)
   (slot years-since-update)
   (slot category)
   (slot access-level)
   (slot completeness)
   (slot verified)
   (slot needs-update (default no))
   (slot status (default none))
   (slot flagged-for-review (default no)))

(defrule rule-needs-update
   ?r <- (record (years-since-update ?y&:(> ?y 1)) (needs-update no))
   =>
   (modify ?r (needs-update yes)))

(defrule rule-pending-verification
   ?r <- (record (completeness incomplete) (status none))
   =>
   (modify ?r (status pending-verification)))

(defrule rule-verification-required
   ?r <- (record (completeness complete) (verified FALSE) (status none))
   =>
   (modify ?r (status pending-verification)))

(defrule rule-flag-confidential
   ?r <- (record (category confidential) (access-level ?a&~restricted) (flagged-for-review no))
   =>
   (modify ?r (flagged-for-review yes)))