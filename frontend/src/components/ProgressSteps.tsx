import { Progress } from "./ui/progress";
import { cn } from "@/lib/utils";
import { MessageSquare, HelpCircle, CheckCircle, Sparkles } from "lucide-react";

export type Step = "query" | "questions" | "answers" | "results";

interface ProgressStepsProps {
  currentStep: Step;
  className?: string;
}

const steps: { key: Step; label: string; stepNumber: number; icon: React.ReactNode }[] = [
  { key: "query", label: "Query", stepNumber: 1, icon: <MessageSquare className="h-3 w-3" /> },
  { key: "questions", label: "Questions", stepNumber: 2, icon: <HelpCircle className="h-3 w-3" /> },
  { key: "answers", label: "Answers", stepNumber: 3, icon: <CheckCircle className="h-3 w-3" /> },
  { key: "results", label: "Results", stepNumber: 4, icon: <Sparkles className="h-3 w-3" /> },
];

export function ProgressSteps({ currentStep, className }: ProgressStepsProps) {
  const currentStepIndex = steps.findIndex(step => step.key === currentStep);
  const progressValue = ((currentStepIndex + 1) / steps.length) * 100;

  return (
    <div className={cn("hidden sm:block w-full bg-surface-50 border-b border-surface-300 py-4", className)}>
      <div className="max-w-2xl mx-auto px-4">
        <div className="flex items-center justify-between mb-3">
          {steps.map((step, index) => (
            <div key={step.key} className="flex items-center">
              <div
                className={cn(
                  "flex items-center justify-center w-8 h-8 rounded-full transition-all duration-300 border-2",
                  index <= currentStepIndex
                    ? "bg-primary text-white border-primary shadow-sm"
                    : "bg-surface-100 text-neutral-400 border-surface-300"
                )}
              >
                {index <= currentStepIndex ? step.icon : <span className="text-xs font-medium">{step.stepNumber}</span>}
              </div>
              <span
                className={cn(
                  "ml-2 text-sm font-medium transition-colors duration-300",
                  index <= currentStepIndex
                    ? "text-neutral-800"
                    : "text-neutral-400"
                )}
              >
                {step.label}
              </span>
              {index < steps.length - 1 && (
                <div className={cn(
                  "w-8 h-0.5 mx-4 transition-colors duration-300",
                  index < currentStepIndex ? "bg-primary-600" : "bg-gray-200"
                )} />
              )}
            </div>
          ))}
        </div>
        <Progress 
          value={progressValue} 
          className="h-1 bg-gray-200" 
        />
      </div>
    </div>
  );
}
