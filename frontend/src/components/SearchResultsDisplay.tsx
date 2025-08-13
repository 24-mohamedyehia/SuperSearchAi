import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Button } from "./ui/button";
import { Badge } from "./ui/badge";
import { Dialog, DialogContent } from "./ui/dialog";
import {
  ExternalLink,
  ChevronLeft,
  ChevronRight,
  X,
  Image as ImageIcon,
  Link,
  BookOpen,
} from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface SearchResultsDisplayProps {
  report: {
    title: string;
    answer: string;
  };
  images?: string[];
  resources?: Array<{
    title: string;
    url: string;
  }>;
  userDetails?: string;
}

export function SearchResultsDisplay({
  report,
  images = [],
  resources = [],
}: SearchResultsDisplayProps) {
  const [imagePreviewOpen, setImagePreviewOpen] = useState(false);
  const [currentImageIndex, setCurrentImageIndex] = useState(0);

  // Remove duplicate images
  const uniqueImages = Array.from(new Set(images));

  const openImagePreview = (index: number) => {
    setCurrentImageIndex(index);
    setImagePreviewOpen(true);
  };

  const nextImage = () => {
    setCurrentImageIndex((prev) => (prev + 1) % uniqueImages.length);
  };

  const prevImage = () => {
    setCurrentImageIndex(
      (prev) => (prev - 1 + uniqueImages.length) % uniqueImages.length
    );
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "ArrowRight") nextImage();
    if (e.key === "ArrowLeft") prevImage();
    if (e.key === "Escape") setImagePreviewOpen(false);
  };

  return (
    <Card className="w-full max-w-4xl bg-surface-50 border-surface-300">
      <CardHeader className="pb-6">
        <CardTitle className="text-xl font-bold text-neutral-900 flex items-center gap-3">
          <div className="h-8 w-8 rounded-full bg-primary flex items-center justify-center">
            <BookOpen className="h-4 w-4 text-white" />
          </div>
          {report.title}
        </CardTitle>
      </CardHeader>

      <CardContent className="space-y-8">
        {/* Images Section */}
        {uniqueImages.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 text-sm font-semibold text-neutral-900">
              <div className="h-6 w-6 rounded-full bg-warning flex items-center justify-center">
                <ImageIcon className="h-3 w-3 text-white" />
              </div>
              Related Images ({uniqueImages.length})
            </div>
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-3">
              {uniqueImages.slice(0, 8).map((image, index) => (
                <div
                  key={index}
                  className="relative aspect-square bg-surface-100 rounded-xl overflow-hidden cursor-pointer hover:scale-105 transition-transform group ring-2 ring-transparent hover:ring-primary-200"
                  onClick={() => openImagePreview(index)}
                >
                  <img
                    src={image}
                    alt={`Related image ${index + 1}`}
                    className="w-full h-full object-cover"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.parentElement!.style.display = "none";
                    }}
                  />
                  <div className="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                    <ImageIcon className="h-6 w-6 text-white drop-shadow-lg" />
                  </div>
                </div>
              ))}
              {uniqueImages.length > 8 && (
                <div
                  className="aspect-square bg-gray-100 rounded-xl flex items-center justify-center cursor-pointer hover:scale-105 transition-transform ring-2 ring-transparent hover:ring-primary-200"
                  onClick={() => openImagePreview(8)}
                >
                  <div className="text-center text-sm text-neutral-600">
                    <ImageIcon className="h-6 w-6 mx-auto mb-1" />
                    <span className="font-medium">
                      +{uniqueImages.length - 8} more
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Report Section */}
        <div className="space-y-4">
          <div className="flex items-center gap-3 text-sm font-semibold text-neutral-900">
            <div className="h-6 w-6 rounded-full bg-primary flex items-center justify-center">
              <BookOpen className="h-3 w-3 text-white" />
            </div>
            Report
          </div>
          <div className="prose prose-sm max-w-none">
            <div className="bg-primary-50 rounded-xl p-6 border border-primary-200">
              <div className="text-sm leading-7 text-neutral-800 font-medium">
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({ children }) => (
                      <h1 className="text-lg font-bold mb-4 text-neutral-900">
                        {children}
                      </h1>
                    ),
                    h2: ({ children }) => (
                      <h2 className="text-md font-semibold mb-3 text-neutral-900">
                        {children}
                      </h2>
                    ),
                    h3: ({ children }) => (
                      <h3 className="text-sm font-semibold mb-2 text-neutral-900">
                        {children}
                      </h3>
                    ),
                    p: ({ children }) => (
                      <p className="mb-3 last:mb-0">{children}</p>
                    ),
                    strong: ({ children }) => (
                      <strong className="font-semibold text-neutral-900">
                        {children}
                      </strong>
                    ),
                    em: ({ children }) => (
                      <em className="italic">{children}</em>
                    ),
                    ul: ({ children }) => (
                      <ul className="list-disc list-inside mb-3 space-y-1">
                        {children}
                      </ul>
                    ),
                    ol: ({ children }) => (
                      <ol className="list-decimal list-inside mb-3 space-y-1">
                        {children}
                      </ol>
                    ),
                    li: ({ children }) => (
                      <li className="text-neutral-800">{children}</li>
                    ),
                    blockquote: ({ children }) => (
                      <blockquote className="border-l-4 border-primary-300 pl-4 italic bg-primary-25 py-2 my-3 rounded-r">
                        {children}
                      </blockquote>
                    ),
                    code: ({ children }) => (
                      <code className="bg-neutral-100 px-1 py-0.5 rounded text-xs font-mono">
                        {children}
                      </code>
                    ),
                    pre: ({ children }) => (
                      <pre className="bg-neutral-100 p-3 rounded-lg overflow-x-auto text-xs font-mono my-3">
                        {children}
                      </pre>
                    ),
                  }}
                >
                  {`# ${report.title}\n\n${report.answer}`}
                </ReactMarkdown>
              </div>
            </div>
          </div>
        </div>

        {/* Resources Section */}
        {resources.length > 0 && (
          <div className="space-y-4">
            <div className="flex items-center gap-3 text-sm font-semibold text-neutral-900">
              <div className="h-6 w-6 rounded-full bg-success flex items-center justify-center">
                <Link className="h-3 w-3 text-white" />
              </div>
              Sources ({resources.length})
            </div>
            <div className="grid gap-3">
              {resources.map((resource, index) => (
                <div
                  key={index}
                  className="flex items-center gap-4 p-4 bg-surface-100 rounded-xl hover:bg-surface-200 transition-all group border border-surface-300 hover:border-surface-400"
                >
                  <div className="flex-1 min-w-0">
                    <a
                      href={resource.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="text-sm font-semibold text-primary hover:text-primary-700 transition-colors line-clamp-1 group-hover:underline"
                    >
                      {resource.title}
                    </a>
                    <p className="text-xs text-neutral-500 mt-1 line-clamp-1">
                      {new URL(resource.url).hostname}
                    </p>
                  </div>
                  <Button
                    variant="ghost"
                    size="sm"
                    className="h-9 w-9 p-0 opacity-60 group-hover:opacity-100 transition-all hover:bg-primary-50 hover:text-primary"
                    onClick={() => window.open(resource.url, "_blank")}
                  >
                    <ExternalLink className="h-4 w-4" />
                  </Button>
                </div>
              ))}
            </div>
          </div>
        )}
      </CardContent>

      {/* Image Preview Modal */}
      <Dialog open={imagePreviewOpen} onOpenChange={setImagePreviewOpen}>
        <DialogContent
          className="max-w-4xl w-full h-[90vh] p-0 bg-black/95 border-none"
          onKeyDown={handleKeyDown}
        >
          <div className="relative w-full h-full flex items-center justify-center">
            {/* Close Button */}
            <Button
              variant="ghost"
              size="sm"
              className="absolute top-4 right-4 z-10 text-white hover:bg-white/20"
              onClick={() => setImagePreviewOpen(false)}
            >
              <X className="h-4 w-4" />
            </Button>

            {/* Navigation Buttons */}
            {uniqueImages.length > 1 && (
              <>
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute left-4 top-1/2 -translate-y-1/2 z-10 text-white hover:bg-white/20"
                  onClick={prevImage}
                >
                  <ChevronLeft className="h-6 w-6" />
                </Button>
                <Button
                  variant="ghost"
                  size="sm"
                  className="absolute right-4 top-1/2 -translate-y-1/2 z-10 text-white hover:bg-white/20"
                  onClick={nextImage}
                >
                  <ChevronRight className="h-6 w-6" />
                </Button>
              </>
            )}

            {/* Image Counter */}
            {uniqueImages.length > 1 && (
              <div className="absolute bottom-4 left-1/2 -translate-x-1/2 z-10">
                <Badge variant="secondary" className="bg-black/50 text-white">
                  {currentImageIndex + 1} / {uniqueImages.length}
                </Badge>
              </div>
            )}

            {/* Current Image */}
            {uniqueImages[currentImageIndex] && (
              <img
                src={uniqueImages[currentImageIndex]}
                alt={`Preview ${currentImageIndex + 1}`}
                className="max-w-full max-h-full object-contain"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.style.display = "none";
                }}
              />
            )}
          </div>
        </DialogContent>
      </Dialog>
    </Card>
  );
}
