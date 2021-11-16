(require "cl-csv")
(defparameter results (cl-csv:read-csv #P"results.csv"))
(defparameter results_list ())
(defparameter time_values ())
(defparameter time_numbers ())
(defparameter score_values ())
(defparameter score ())
(defparameter expected_value_time 0)
(defparameter mean_score 0)
(defparameter variance_score 0)

(loop for a in results
   do (if (string-equal (NTH 0 a) "0")
             (push a results_list)))

(loop for a in results_list
   do (push (String-left-trim "0:00:" (NTH 2 a)) time_values))

(loop for a in results_list
   do (push (NTH 3 a) score_values))

(loop for a in time_values
   do (push (NTH 0 (with-input-from-string (in a)
  (loop for x = (read in nil nil) while x collect x))) time_numbers))

(loop for a in score_values
   do (push (NTH 0 (with-input-from-string (in a)
  (loop for x = (read in nil nil) while x collect x))) score))

(setq expected_value_time (/ (apply '+ time_numbers) (length time_numbers)))

(setq mean_score (/ (apply '+ score) (length score)))

(setq variance_score (/ (apply '+ (mapcar (lambda (x) (* x x)) (mapcar (lambda (n) (- n mean_score))
        score))) (length score)))

expected_value_time
variance_score
